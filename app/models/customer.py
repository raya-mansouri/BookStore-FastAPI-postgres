from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from fastapi import HTTPException
import pytz
from .base import Base

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    subscription_model = Column(Enum("free", "plus", "premium", name="subscription_models"), nullable=False)
    subscription_end_time = Column(DateTime)
    wallet_money_amount = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="customer")
    reservations = relationship("Reservation", back_populates="customer", cascade="all, delete-orphan")

    def charge_wallet(self, amount: int):
        """Increase the wallet balance by the given amount."""
        self.wallet_money_amount += amount

    def upgrade_subscription(self, new_model: str):
        pre_wallet_amount = self.wallet_money_amount
        pre_subscription_model = self.subscription_model
        iran_timezone = pytz.timezone('Asia/Tehran')
        now = datetime.now(iran_timezone)

        cost_mapping = {
            ("free", "plus"): 50000,
            ("plus", "premium"): 150000,
            ("free", "premium"): 200000
        }
        duration = timedelta(days=30)  # Both "plus" and "premium" last for 1 month

        cost = cost_mapping.get((pre_subscription_model, new_model))
        if cost is None:
            raise ValueError("Invalid subscription upgrade path")

        if pre_wallet_amount < cost:
            raise HTTPException(status_code=400, detail="Insufficient wallet balance")

        self.wallet_money_amount -= cost
        self.subscription_model = new_model
        self.subscription_end_time = now + duration