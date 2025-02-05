from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, LoginStep1Request, LoginStep2Request, Token
from app.services.auth_service import AuthService
from app.dependency import get_db
from config import settings

 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db=Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register_user(user_data)

@router.post("/login/step1")
async def login_step1(credentials: LoginStep1Request, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.login_step1(credentials)

@router.post("/login/step2", response_model=Token)
async def login_step2(otp_data: LoginStep2Request, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.login_step2(otp_data)

# @router.get("/mock-otp/{user_id}")
# async def get_mock_otp(user_id: str, db=Depends(get_db)):
#     auth_service = AuthService(db)
#     return {"otp": auth_service.otp_storage.get(user_id, "No OTP generated")}