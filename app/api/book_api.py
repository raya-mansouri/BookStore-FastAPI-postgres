from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.book import BookCreate, BookUpdate, BookBase
from app.services.book_service import BookService
from app.dependency import get_db

router = APIRouter()

@router.post("/", response_model=BookCreate)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    service = BookService(db)
    book = service.create_book(book_data)
    
    # Convert the Book SQLAlchemy model to the BookCreate schema
    book_create = BookCreate(
        title=book.title,
        isbn=book.isbn,
        price=book.price,
        genre_id=book.genre_id,
        description=book.description,
        units=book.units,
        author_ids=[author.id for author in book.authors]  # Populate author_ids
    )
    
    return book_create

@router.get("/{book_id}", response_model=BookBase)
def get_book(book_id: int, db: Session = Depends(get_db)):
    service = BookService(db)
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Convert the Book SQLAlchemy model to the BookResponse schema
    book_response = BookBase(
        id=book.id,
        title=book.title,
        isbn=book.isbn,
        price=book.price,
        genre_id=book.genre_id,
        description=book.description,
        units=book.units,
        reserved_units=book.reserved_units,
        author_ids=[author.id for author in book.authors]  # Populate author_ids
    )
    
    return book_response

# @router.put("/{book_id}", response_model=BookUpdate)
# def update_book(book_id: int, update_data: BookUpdate, db: Session = Depends(get_db)):
#     service = BookService(db)
#     return service.update_book(book_id, update_data)

# @router.delete("/{book_id}")
# def delete_book(book_id: int, db: Session = Depends(get_db)):
#     service = BookService(db)
#     service.delete_book(book_id)
#     return {"message": "Book deleted successfully"}