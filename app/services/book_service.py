from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException, status
from typing import Dict, Any
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from app.schemas.book import BookCreate, BookUpdate, BookOut

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

        return self._prepare_book_out(book)

    def get_book(self, book_id: int) -> Book:
        try:
            book = self.db.query(Book).filter(Book.id == book_id).first()
            return self._prepare_book_out(book)
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found.",
            )

    def get_all_books(self, skip: int = 0, limit: int = 100) -> list[BookOut]:
        try:
            db_books = (
                self.db.query(Book)
                .options(selectinload(Book.authors))  # Eagerly load the authors relationship
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [self._prepare_book_out(db_book) for db_book in db_books]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving books: {str(e)}",
            )

    def update_book(self, book_id: int, book: BookUpdate) -> BookOut:
        try:
            db_book = (
                self.db.query(Book)
                .options(selectinload(Book.authors))  # Eagerly load the authors relationship
                .filter(Book.id == book_id)
                .one()
            )
            update_data = book.model_dump(exclude_unset=True)

            # Validate genre_id if provided
            if "genre_id" in update_data:
                genre = self.db.query(Genre).filter(Genre.id == update_data["genre_id"]).first()
                if not genre:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Genre with ID {update_data['genre_id']} not found."
                    )

            # Validate author_ids if provided
            if "author_ids" in update_data:
                invalid_author_ids = []
                for author_id in update_data["author_ids"]:
                    author = self.db.query(Author).filter(Author.id == author_id).first()
                    if not author:
                        invalid_author_ids.append(author_id)

                if invalid_author_ids:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Authors with IDs {invalid_author_ids} not found."
                    )

                # Update authors (many-to-many relationship)
                db_book.authors = []
                for author_id in update_data["author_ids"]:
                    author = self.db.query(Author).get(author_id)
                    db_book.authors.append(author)
                del update_data["author_ids"]  # Remove author_ids from update_data to avoid conflict

            for key, value in update_data.items():
                setattr(db_book, key, value)

            self.db.commit()
            self.db.refresh(db_book)
            return self._prepare_book_out(db_book)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found.",
            )
        except IntegrityError as e:
            self.db.rollback()
            if "isbn" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ISBN already exists.",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while updating the book.",
                )

    def patch_book(self, book_id: int, update_data: dict[str, Any]) -> BookOut:
        try:
            # Fetch the book from the database
            db_book = (
                self.db.query(Book)
                .options(selectinload(Book.authors))  # Eagerly load authors
                .filter(Book.id == book_id)
                .one()
            )

            # Validate genre_id if provided
            if "genre_id" in update_data:
                genre = self.db.query(Genre).filter(Genre.id == update_data["genre_id"]).first()
                if not genre:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Genre with ID {update_data['genre_id']} not found."
                    )

            # Validate author_ids if provided
            if "author_ids" in update_data:
                invalid_author_ids = []
                for author_id in update_data["author_ids"]:
                    author = self.db.query(Author).filter(Author.id == author_id).first()
                    if not author:
                        invalid_author_ids.append(author_id)

                if invalid_author_ids:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Authors with IDs {invalid_author_ids} not found."
                    )

                # Update authors (many-to-many relationship)
                db_book.authors = []
                for author_id in update_data["author_ids"]:
                    author = self.db.query(Author).get(author_id)
                    db_book.authors.append(author)
                del update_data["author_ids"]  # Remove author_ids to avoid conflict

            # Check for duplicate ISBN if isbn is being updated
            if "isbn" in update_data and update_data["isbn"] != db_book.isbn:
                existing_book = self.db.query(Book).filter(Book.isbn == update_data["isbn"]).first()
                if existing_book:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="A book with this ISBN already exists."
                    )

            # Update only the fields provided in update_data
            for key, value in update_data.items():
                setattr(db_book, key, value)

            # Commit changes to the database
            self.db.commit()
            self.db.refresh(db_book)

            # Return the updated book as a BookOut schema
            return self._prepare_book_out(db_book)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found.",
            )
        except IntegrityError as e:
            self.db.rollback()
            if "isbn" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ISBN already exists.",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while updating the book.",
                )

    def _prepare_book_out(self, book: Book) -> BookOut:
        """
        Helper method to convert a Book model instance to a BookOut schema.
        """
        return BookOut(
            id=book.id,
            title=book.title,
            isbn=book.isbn,
            price=book.price,
            genre_id=book.genre_id,
            description=book.description,
            units=book.units,
            author_ids=[author.id for author in book.authors]  # Populate author_ids
        )
    def delete_book(self, book_id: int) -> None:
        try:
            db_book = self.db.query(Book).filter(Book.id == book_id).one()
            self.db.delete(db_book)
            self.db.commit()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found.",
            )

    def _prepare_book_out(self, book: Book) -> BookOut:
        """
        Helper method to prepare a BookOut object from a Book model instance.
        """
        return BookOut(
            id=book.id,
            title=book.title,
            isbn=book.isbn,
            price=book.price,
            genre_id=book.genre_id,
            description=book.description,
            units=book.units,
            author_ids=[author.id for author in book.authors]  # Populate author_ids
        )