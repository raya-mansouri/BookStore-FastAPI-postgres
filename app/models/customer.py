from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Numeric
from sqlalchemy.orm import relationship
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