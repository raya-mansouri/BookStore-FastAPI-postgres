from pydantic import BaseModel, Field
from datetime import datetime

class ReservationCreateSchema(BaseModel):
    book_id: int = Field(..., description="ID of the book to reserve")
    days: int = Field(..., description="Number of days for reservation")

class ReservationResponseSchema(BaseModel):
    id: int
    customer_id: int
    book_id: int
    start_of_reservation: datetime
    end_of_reservation: datetime
    status: str

class QueueResponseSchema(BaseModel):
    customer_id: int
    book_id: int
    queue_position: int
