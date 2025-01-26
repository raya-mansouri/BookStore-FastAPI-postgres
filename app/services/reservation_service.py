from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.customer import Customer
from app.models.reservation import Reservation

class ReservationService:
    def __init__(self, db: Session):
        self.db = db

    # def _calculate_price(self, customer: Customer, days: int) -> int:
    #     base_price = days * 1000  # 1000 Toman per day
        # Apply 30% discount if >3 books in the last 30 days
        # Apply 100% discount if >300,000 Toman spent in 60 days
        # return final_price

    def reserve_book(self, customer_id: int, book_id: int, days: int) -> Reservation:
        customer = self.db.query(Customer).get(customer_id)
        book = self.db.query(Book).get(book_id)

        # Check subscription tier, wallet balance, and reservation limits
        if customer.subscription_model == "free":
            raise HTTPException(status_code=403, detail="Free users cannot reserve books.")

        # Calculate price with discounts
        price = self._calculate_price(customer, days)

        # Handle instant/scheduled reservation
        if book.units > 0:
            return self._instant_reserve(customer, book, days, price)
        else:
            return self._scheduled_reserve(customer, book, days, price)