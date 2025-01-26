from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from app.schemas.book import BookCreate

class BookService:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book_data: BookCreate) -> Book:
        # Check for duplicate ISBN
        existing_book = self.db.query(Book).filter(Book.isbn == book_data.isbn).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A book with this ISBN already exists."
            )

        # Validate genre_id
        genre = self.db.query(Genre).filter(Genre.id == book_data.genre_id).first()
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with ID {book_data.genre_id} not found."
            )

        # Validate author_ids
        invalid_author_ids = []
        for author_id in book_data.author_ids:
            author = self.db.query(Author).filter(Author.id == author_id).first()
            if not author:
                invalid_author_ids.append(author_id)

        if invalid_author_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Authors with IDs {invalid_author_ids} not found."
            )

        # Create the book
        book = Book(
            title=book_data.title,
            isbn=book_data.isbn,
            price=book_data.price,
            genre_id=book_data.genre_id,
            description=book_data.description,
            units=book_data.units
        )
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)

        # Add authors to the book (many-to-many relationship)
        for author_id in book_data.author_ids:
            author = self.db.query(Author).get(author_id)
            book.authors.append(author)
        self.db.commit()
        self.db.refresh(book)

        return book

    # def get_book(self, book_id: int) -> Book:
    #     return self.db.query(Book).filter(Book.id == book_id).first()
    
    # def get_all_books(self) -> list[Book]:
    #     return self.db.query(Book).all()

    # def update_book(self, book_id: int, update_data: BookUpdate) -> Book:
    #     book = self.get_book(book_id)
    #     for key, value in update_data.dict().items():
    #         setattr(book, key, value)
    #     self.db.commit()
    #     self.db.refresh(book)
    #     return book

    # def delete_book(self, book_id: int) -> None:
    #     book = self.get_book(book_id)
    #     self.db.delete(book)
    #     self.db.commit()