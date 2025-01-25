from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class BookAuthor(Base):
    __tablename__ = "book_author"
    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"), primary_key=True)

    # Relationships
    book = relationship("Book", back_populates="authors")
    author = relationship("Author", back_populates="books")