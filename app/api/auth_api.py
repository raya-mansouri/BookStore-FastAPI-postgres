from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.book import BookCreate
from app.services.book_service import BookService
from app.dependency import get_db

router = APIRouter()

# @router.post("/auth/signup")
# def signup(user_data: UserCreate, db: Session = Depends(get_db)):
#     service = AuthService(db)
#     return service.signup(user_data)

# @router.post("/auth/login")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     service = AuthService(db)
#     return service.login(username, password)