from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from pytz import timezone
from typing import Optional
import secrets, redis, os
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import UserCreate, LoginStep1Request, LoginStep2Request
from app.models.user import User
from app.schemas.auth import TokenData
from config import settings
 
SECRET_KEY =  settings.SECRET_KEY
ALGORITHM =  settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        # self.otp_storage: Dict[str, str] = {}  # user_id: otp
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        iran_timezone = timezone('Asia/Tehran')
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(iran_timezone) + expires_delta
        else:
            expire = datetime.now(iran_timezone) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def generate_otp(self, user_id: str):
        otp = secrets.randbelow(999999)
        otp_code = f"{otp:06d}"
        # self.otp_storage[user_id] = otp_code
        self.redis.set(otp_code, user_id, ex=300)  #
        print(f"OTP for {user_id}: {otp_code}")  # Mock SMS service
        return otp_code

    def verify_otp(self, otp: str):
        # stored_otp = self.otp_storage.get(user_id)
        # if not stored_otp:
        #     return False
        # return secrets.compare_digest(otp, stored_otp)
        user_id = self.redis.get(otp)
        if not user_id:
            return None
        return user_id.decode('utf-8')
    

    def register_user(self, user_data: UserCreate):
        # Check if username or email already exists in a single query
        existing_user = self.db.query(User).filter(
            or_(User.username == user_data.username, User.email == user_data.email)
        ).first()

        if existing_user:
            # Determine which field caused the conflict
            if existing_user.username == user_data.username:
                raise HTTPException(status_code=400, detail="Username already registered")
            elif existing_user.email == user_data.email:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = self.get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            password=hashed_password,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            role=user_data.role,
            is_active=True
        )
        self.db.add(new_user)
        self.db.flush() 
        self.db.commit()
        return {"message": "User created successfully"}

    async def authenticate_user(self, username: str, password: str):
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not self.verify_password(password, user.password):
            return False
        return user
    
    async def login_step1(self, credentials: LoginStep1Request):
        """
        Authenticate the user and generate an OTP.
        """
        user = await self.authenticate_user(credentials.username, credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        otp = self.generate_otp(user.id)
        return {"message": "OTP sent to your registered mobile number", "otp": otp}

    async def login_step2(self, otp_data: LoginStep2Request):
        """
        Verify the OTP and generate an access token.
        """
        user_id = self.verify_otp(otp_data.otp)
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"id": user.id, "sub": user.username, "role": user.role},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id: int = payload.get("id")
            username: str = payload.get("sub")
            role: str = payload.get("role")
            if username is None or role is None or id is None:
                raise credentials_exception
            token_data = TokenData(username=username, role=role)
        except JWTError:
            raise credentials_exception

        user = self.db.query(User).filter(User.username == token_data.username).first()
        if user is None:
            raise credentials_exception
        return user