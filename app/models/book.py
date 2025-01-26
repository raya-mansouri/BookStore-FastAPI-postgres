from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base
from .book_author import BookAuthor

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    price = Column(Integer, nullable=False, default=0)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    description = Column(Text)
    units = Column(Integer, nullable=False)
    reserved_units = Column(Integer, default=0, nullable=False)

    # Relationships
    genre = relationship("Genre")
    authors = relationship("Author", secondary=BookAuthor, back_populates="books")
    reservations = relationship("Reservation", back_populates="book", cascade="all, delete-orphan")