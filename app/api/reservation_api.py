from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from app.dependency import get_db
from app.permissions import extract_user_id
from app.schemas.reservation import *
from app.services.auth_service import AuthService
from app.services.reservation_service import ReservationService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

get_current_user  =AuthService.get_current_user

@router.post("/reserve", response_model=ReservationResponseSchema | QueueResponseSchema, status_code=status.HTTP_201_CREATED)
@extract_user_id
async def reserve_book(
    reservation_data: ReservationCreateSchema,
    user_id: int = None,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)):

    book_id = reservation_data.book_id
    days = reservation_data.days
    
    service = ReservationService(db, user_id=user_id, book_id=book_id, days=days)
    return service.reserve()

# @router.get("/reservations", response_model=List[ReservationResponseSchema])
# def list_reservations(user_id: int = Depends(get_current_user)):
#     return ReservationService.get_user_reservations(user_id)

@router.delete("/cancel/{reservation_id}")
def cancel_reservation(reservation_id: int, 
                        user_id: int = None,
                        token: str = Depends(oauth2_scheme),
                        db: Session = Depends(get_db)):
    service = ReservationService(db, user_id=user_id)
    return service.cancel_reservation(reservation_id)

# @router.get("/queue/{book_id}", response_model=ReservationQueueSchema)
# def get_reservation_queue_position(book_id: int, user_id: int = Depends(get_current_user)):
#     return ReservationService.get_queue_position(user_id, book_id)