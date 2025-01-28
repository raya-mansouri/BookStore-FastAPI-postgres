# permissions.py
from fastapi import HTTPException, status
from functools import wraps
from jose import jwt
from jose.exceptions import JWTError
from app.schemas.auth import TokenData
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Decode JWT token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(username=payload.get("sub"), role=payload.get("role"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

# Permission decorator for Admin
def admin_only(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        token_data = decode_token(token)
        if token_data.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can access this endpoint",
            )
        return await func(*args, **kwargs)
    return wrapper

# Permission decorator for Customer
def customer_only(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        token_data = decode_token(token)
        if token_data.role != "customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can access this endpoint",
            )
        return await func(*args, **kwargs)
    return wrapper

# Permission decorator for Author
def author_only(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        token_data = decode_token(token)
        if token_data.role != "author":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only authors can access this endpoint",
            )
        return await func(*args, **kwargs)
    return wrapper