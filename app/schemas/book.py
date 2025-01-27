from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class BookBase(BaseModel):
    """
    Base schema for book-related models.
    Contains shared fields and validators.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The title of the book.",
        example="The Great Gatsby"
    )
    isbn: str = Field(
        ...,
        pattern=r"^\d{13}$",
        description="The ISBN-13 of the book (must be exactly 13 digits and unique).",
        example="9783161484100"
    )
    price: int = Field(
        ...,
        gt=0,
        description="The price of the book in Toman (must be greater than 0).",
        example=29000
    )
    genre_id: int = Field(
        ...,
        description="The ID of the genre the book belongs to.",
        example=1
    )
    description: Optional[str] = Field(
        "No description provided",
        min_length=10,
        max_length=1000,
        description="A brief description of the book (optional).",
        example="A classic novel about the American Dream."
    )
    units: int = Field(
        ...,
        ge=0,
        description="The number of available units of the book (must be 0 or greater).",
        example=10
    )
    author_ids: List[int] = Field(
        ...,
        min_items=1,
        description="A list of author IDs for the book (must have at least one author).",
        example=[1, 2]
    )

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        """
        Validate that the title is not empty and is properly formatted.
        """
        if not value.strip():
            raise ValueError("Title cannot be empty or just whitespace.")
        return value.strip()

    @field_validator("isbn")
    def validate_isbn(cls, value: str) -> str:
        """
        Validate that the ISBN is exactly 13 digits.
        """
        if not value.isdigit() or len(value) != 13:
            raise ValueError("ISBN must be exactly 13 digits.")
        return value

    @field_validator("author_ids")
    def validate_author_ids(cls, value: List[int]) -> List[int]:
        """
        Validate that there is at least one author ID.
        """
        if not value:
            raise ValueError("At least one author ID is required.")
        return value
    
    class Config:
        from_attributes = True

class BookCreate(BookBase):
    """
    Represents the data required to create a new book.
    Inherits fields and validators from BookBase.
    """
    pass


class BookUpdate(BookBase):
    """
    Represents the data that can be updated for a book.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="The title of the book.",
        example="The Great Gatsby"
    )
    isbn: Optional[str] = Field(
        None,
        pattern=r"^\d{13}$",
        description="The ISBN-13 of the book (must be exactly 13 digits and unique).",
        example="9783161484100"
    )
    price: Optional[int] = Field(
        None,
        gt=0,
        description="The price of the book in Toman (must be greater than 0).",
        example=29000
    )
    genre_id: Optional[int] = Field(
        None,
        description="The ID of the genre the book belongs to.",
        example=1
    )
    description: Optional[str] = Field(
        None,
        min_length=10,
        max_length=1000,
        description="A brief description of the book (optional).",
        example="A classic novel about the American Dream."
    )
    units: Optional[int] = Field(
        None,
        ge=0,
        description="The number of available units of the book (must be 0 or greater).",
        example=10
    )
    author_ids: Optional[List[int]] = Field(
        None,
        min_items=1,
        description="A list of author IDs for the book (must have at least one author).",
        example=[1, 2]
    )

from pydantic import field_validator

class BookOut(BookBase):
    id: int

    @field_validator("author_ids", mode="before")
    def extract_author_ids(cls, value, values):
        if isinstance(value, list):
            return value  # If author_ids is already a list, return it
        elif hasattr(value, "authors"):  # If value is a Book model with authors relationship
            return [author.id for author in value.authors]  # Extract author IDs
        else:
            return []  # Default to an empty list

    class Config:
        from_attributes = True