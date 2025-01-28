from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.permissions import admin_only, author_only
from app.schemas.book import BookCreate, BookUpdate, BookOut
from app.services.book_service import BookService

from app.dependency import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
@admin_only
async def create_book(book_data: BookCreate,
                token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
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
@author_only
def update_book(book_id: int, update_data: BookUpdate,
                token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
    service = BookService(db)
    return service.update_book(book_id, update_data)

@router.patch("/{book_id}", response_model=BookOut)
@author_only
def update_book(book_id: int, update_data: BookUpdate,
                token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
    service = BookService(db)
    return service.update_book(book_id, update_data)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@author_only
def delete_book(book_id: int, 
                token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
    service = BookService(db)
    service.delete_book(book_id)
    return {"message": "Book deleted successfully"}