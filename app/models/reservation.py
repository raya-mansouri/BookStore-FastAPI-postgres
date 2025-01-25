from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Enum
from sqlalchemy.orm import relationship
from .base import Base

class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    start_of_reservation = Column(DateTime, nullable=False)
    end_of_reservation = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum("pending", "active", "completed", name="reservation_status"), default="pending")
    queue_position = Column(Integer, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")