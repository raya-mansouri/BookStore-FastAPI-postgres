from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.schemas.auth import UserCreate, LoginStep1Request, LoginStep2Request, Token
from app.services.auth_service import AuthService
from app.dependency import get_db
from app.models.user import User
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) 

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db=Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register_user(user_data)

@router.post("/login/step1")
async def login_step1(credentials: LoginStep1Request, db=Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    otp = auth_service.generate_otp(user.id)
    return {"message": "OTP sent to your registered mobile number", "otp": otp}

@router.post("/login/step2", response_model=Token)
async def login_step2(otp_data: LoginStep2Request, db=Depends(get_db)):
    auth_service = AuthService(db)

    user_id = auth_service.verify_otp(otp_data.otp) 
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"id": user_id, "sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/mock-otp/{user_id}")
# async def get_mock_otp(user_id: str, db=Depends(get_db)):
#     auth_service = AuthService(db)
#     return {"otp": auth_service.otp_storage.get(user_id, "No OTP generated")}