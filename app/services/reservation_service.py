from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import redis
from app.schemas.reservation import QueueResponseSchema
from app.models.book import Book
from app.models.customer import Customer
from app.models.reservation import Reservation

redis_client = redis.Redis(host='localhost', port=6379, db=1)


class ReservationService:
    def __init__(self, db: Session, user_id: int, book_id: int, days: int):
        self.db = db
        self.customer = self._get_customer(user_id)
        self.book = self._get_book(book_id)
        self.days = days
        self.validate_reservation()
    
    def _get_customer(self, user_id):
        customer = self.db.query(Customer).filter_by(user_id=user_id).first()
        if not customer:
            raise HTTPException("Customer not found")
        return customer
    
    def _get_book(self, book_id):
        book = self.db.query(Book).filter_by(id=book_id).first()
        if not book:
            raise HTTPException("Book not found")
        return book
    
    def validate_reservation(self):
        if self.customer.subscription_model == "free":
            raise HTTPException("Free users cannot reserve books")
        
        max_days = 14 if self.customer.subscription_model == "premium" else 7
        if self.days > max_days:
            raise HTTPException("Exceeding reservation limit for subscription tier")
        
        max_units = 10 if self.customer.subscription_model == "premium" else 5
        active_reservations = self.db.query(Reservation).filter_by(customer_id=self.customer.id, status="active").count()
        if active_reservations >= max_units:
            raise HTTPException("Reservation limit exceeded")
        
        self.check_funds()
    
    def check_funds(self):
        daily_rate = 1000
        total_cost = self.days * daily_rate
        # Apply 30% discount if >3 books in the last 30 days
        # Apply 100% discount if >300,000 Toman spent in 60 days
        if self.customer.wallet_money_amount < total_cost:
            raise HTTPException("Not enough balance. Please recharge.")

    def has_read_more_than_3_books(self) -> bool:
        # Logic to check if the customer has read more than 3 books in the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        books_read = self.db.query(Reservation).filter(
            Reservation.customer_id == self.customer.id,
            Reservation.end_of_reservation >= thirty_days_ago
        ).count()
        return books_read > 3
    
    def has_paid_more_than_300k(self) -> bool:
        # Logic to check if the customer has paid more than 300,000 Toman in the last 60 days
        sixty_days_ago = datetime.utcnow() - timedelta(days=60)
        total_paid = self.db.query(Reservation).filter(
            Reservation.customer_id == self.customer.id,
            Reservation.start_of_reservation >= sixty_days_ago
        ).count() * 1000  # Assuming 1000 Toman per reservation day
        return total_paid > 300000

    def reserve(self):
        if self.book.units - self.book.reserved_units > 0:
            return self.instant_reserve()
        return self.queue_reserve()
    
    def instant_reserve(self):
        self.validate_reservation()
        
        # Deduct cost from wallet
        daily_rate = 1000
        total_cost = self.days * daily_rate
        self.customer.wallet_money_amount -= total_cost
        
        # Update book reserved units
        self.book.reserved_units += 1
        
        # Create reservation
        reservation = Reservation(
            customer_id=self.customer.id,
            book_id=self.book.id,
            start_of_reservation=datetime.utcnow(),
            end_of_reservation=datetime.utcnow() + timedelta(days=self.days),
            price=total_cost,
            status="active"
        )
        self.db.add(reservation)
        self.db.commit()
        return reservation

    def queue_reserve(self):
        # Add to Redis queue
        queue_key = f"reservation_queue:{self.book.id}"
        priority = 0 if self.customer.subscription_model == "premium" else (1 if self.customer.subscription_model == "plus" else 3)
        redis_client.zadd(queue_key, {self.customer.id: priority})
        # return {"message": "Added to reservation queue"}
        queue_position = redis_client.zrank(queue_key, self.customer.id)
        return QueueResponseSchema(
        customer_id=self.customer.id,
        book_id=self.book.id,
        queue_position=queue_position + 1,
    )
    
    def process_queue(self):
        queue_key = f"reservation_queue:{self.book.id}"
        next_customer_id = redis_client.zrange(queue_key, 0, 0, withscores=True)
        if next_customer_id:
            next_customer_id = int(next_customer_id[0][0])
            next_customer = self._get_customer(next_customer_id)
            
            # Check if the customer has sufficient funds
            daily_rate = 1000
            total_cost = self.days * daily_rate
            if next_customer.wallet_money_amount >= total_cost:
                redis_client.zrem(queue_key, next_customer_id)
                return self.instant_reserve()
            else:
                # Remove customer from queue if they don't have enough funds
                redis_client.zrem(queue_key, next_customer_id)
                return self.process_queue()
        return {"message": "No customers in the queue"}

    def cancel_reservation(self, reservation_id: int):
        reservation = self.db.query(Reservation).filter_by(id=reservation_id, customer_id=self.customer.id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        
        # Refund wallet (if applicable)
        if reservation.status == "active":
            refund_amount = (reservation.end_of_reservation - reservation.start_of_reservation).days * 1000
            self.customer.wallet_money_amount += refund_amount
        
        # Update book reserved units
        self.book.reserved_units -= 1
        
        # Update reservation status
        reservation.status = "cancelled"
        self.db.commit()
        return {"message": "Reservation cancelled successfully"}

    