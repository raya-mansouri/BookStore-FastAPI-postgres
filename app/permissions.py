# permissions.py
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from functools import wraps
from jose import jwt
from jose.exceptions import JWTError
from app.schemas.auth import TokenData
from config import settings
import os

 
SECRET_KEY =  settings.SECRET_KEY
ALGORITHM =  settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Decode JWT token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(id=payload.get("id"), username=payload.get("sub"), role=payload.get("role"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def permission_required(allowed_roles=None, allow_current_user=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.pop("token", None)
            if not token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
            
            token_data = decode_token(token)
            kwargs["user_id"] = token_data.id

            if allow_current_user:
                user_id = token_data.id

            if allowed_roles and token_data.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator


