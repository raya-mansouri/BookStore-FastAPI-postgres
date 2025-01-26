from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.book import BookCreate
from app.services.book_service import BookService
from app.dependency import get_db
from app.services.reservation_service import ReservationService

# router = APIRouter()
# @router.delete("/admin/reservations/{reservation_id}")
# def admin_delete_reservation(reservation_id: int, current_user: User = Depends(get_admin_user)):
#     service = ReservationService(db)
#     return service.force_end_reservation(reservation_id)