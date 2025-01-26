from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.book import BookCreate
from app.services.book_service import BookService
from app.dependency import get_db

router = APIRouter()

@router.post("/books")
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.create_book(book_data)

@router.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    service = BookService(db)
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book