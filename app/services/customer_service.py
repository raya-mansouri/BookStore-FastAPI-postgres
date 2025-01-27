from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut

class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, customer_data: CustomerCreate) -> CustomerOut:
        # Check if the user already has a customer profile
        existing_customer = self.db.query(Customer).filter(Customer.user_id == customer_data.user_id).first()
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A customer profile already exists for this user."
            )

        # Create the customer
        customer = Customer(
            user_id=customer_data.user_id,
            subscription_model=customer_data.subscription_model,
            subscription_end_time=customer_data.subscription_end_time,
            wallet_money_amount=customer_data.wallet_money_amount
        )
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return self._prepare_customer_out(customer)

    def get_customer(self, customer_id: int) -> CustomerOut:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found."
            )
        return self._prepare_customer_out(customer)

    def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[CustomerOut]:
        customers = self.db.query(Customer).offset(skip).limit(limit).all()
        return [self._prepare_customer_out(customer) for customer in customers]

    def update_customer(self, customer_id: int, customer_data: CustomerUpdate) -> CustomerOut:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found."
            )

        # Update fields
        for key, value in customer_data.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)
        return self._prepare_customer_out(customer)

    def patch_customer(self, customer_id: int, update_data: dict) -> CustomerOut:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found."
            )

        # Update only the fields provided in update_data
        for key, value in update_data.items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)
        return self._prepare_customer_out(customer)

    def delete_customer(self, customer_id: int) -> None:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found."
            )

        self.db.delete(customer)
        self.db.commit()

    def _prepare_customer_out(self, customer: Customer) -> CustomerOut:
        """
        Helper method to convert a Customer model instance to a CustomerOut schema.
        """
        return CustomerOut(
            id=customer.id,
            user_id=customer.user_id,
            subscription_model=customer.subscription_model,
            subscription_end_time=customer.subscription_end_time,
            wallet_money_amount=customer.wallet_money_amount
        )