from sqlalchemy.orm import Session
# from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status

# class AuthService:
#     def __init__(self, db: Session):
#         self.db = db

#     def signup(self, user_data: UserCreate) -> User:
#         # Validate password, email, phone, etc.
#         # Hash password
#         user = User(**user_data.dict())
#         self.db.add(user)
#         self.db.commit()
#         return user

#     def login(self, username: str, password: str) -> str:
#         # Verify password
#         # Generate OTP and print to console
#         otp = generate_otp()  # e.g., "123456"
#         print(f"OTP for {username}: {otp}")
#         return otp

#     def verify_otp(self, username: str, otp: str) -> str:
#         # Validate OTP and return JWT token
#         access_token = create_access_token(data={"sub": username})
#         return access_token