from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.book import BookCreate, BookUpdate, BookBase, BookOut
from app.services.book_service import BookService
from app.dependency import get_db

router = APIRouter()

@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.create_book(book_data)

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.get_book(book_id)

@router.get("/", response_model=list[BookOut])
def get_all_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = BookService(db)
    return service.get_all_books(skip=skip, limit=limit)

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, update_data: BookUpdate, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.update_book(book_id, update_data)

@router.patch("/{book_id}", response_model=BookOut)
def update_book(book_id: int, update_data: BookUpdate, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.update_book(book_id, update_data)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    service = BookService(db)
    service.delete_book(book_id)
    return {"message": "Book deleted successfully"}