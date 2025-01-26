from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

# Association table
BookAuthor = Table(
    "BookAuthor",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("book.id")),
    Column("author_id", Integer, ForeignKey("author.id")),
    schema="public"
)