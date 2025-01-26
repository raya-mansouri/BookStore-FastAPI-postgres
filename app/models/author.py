from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .book_author import BookAuthor


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    goodreads_link = Column(String(255))
    bank_account_number = Column(String(50), nullable=False)

    # Relationships
    user = relationship("User", back_populates="author")
    city = relationship("City")
    books = relationship("Book", secondary=BookAuthor, back_populates="authors")