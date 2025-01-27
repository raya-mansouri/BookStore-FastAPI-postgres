from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., min_length=11, max_length=11)
    email: EmailStr
    role: str = Field(..., pattern="^(admin|customer|author)$")

    @field_validator("phone")
    def validate_phone(cls, v):
        if not v.startswith("09"):
            raise ValueError("Phone number must start with '09'")
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone: Optional[str] = Field(None, min_length=11, max_length=11)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    role: Optional[str] = Field(None, pattern="^(admin|customer|author)$")
    subscription_end_time: Optional[datetime] = None

class UserOut(UserBase):
    id: int
    subscription_end_time: Optional[datetime] = None

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility