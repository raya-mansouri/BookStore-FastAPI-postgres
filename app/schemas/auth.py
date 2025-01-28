from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    AUTHOR = "author"

class UserBase(BaseModel):
    username: str = Field(..., example="john_doe", description="Unique username for login")
    email: EmailStr = Field(..., example="user@example.com", description="Valid email address")
    first_name: str = Field(..., example="John", description="User's first name")
    last_name: str = Field(..., example="Doe", description="User's last name")
    phone: str = Field(..., example="09123456789", 
                      description="Iranian phone number starting with 09, 11 digits")
    role: UserRole = Field(..., example=UserRole.CUSTOMER, description="User role")

class UserCreate(UserBase):
    password: str = Field(..., example="strongpassword123", 
                         min_length=8, description="Password with minimum 8 characters")

class UserResponse(UserBase):
    id: int
    is_active: bool
    subscription_end_time: datetime | None
    wallet_money_amount: int

    class Config:
        orm_mode = True

class LoginStep1Request(BaseModel):
    username: str = Field(..., example="john_doe")
    password: str = Field(..., example="strongpassword123")

class LoginStep2Request(BaseModel):
    otp: str = Field(..., example="123456", min_length=6, max_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None
    username: str | None = None
    role: str | None = None