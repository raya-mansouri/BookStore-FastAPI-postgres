from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.permissions import extract_user_id
from app.services.purchase_service import PurchaseService

from app.dependency import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.patch("/charge-wallet", status_code=status.HTTP_204_NO_CONTENT)
@extract_user_id
async def charge_wallet(amount: int,
                        user_id: int = None,
                        token: int = Depends(oauth2_scheme),
                        db: Session = Depends(get_db)):
    service = PurchaseService(db)
    return service.charge_wallet(user_id, amount)

@router.patch("/upgrade-subscription", status_code=status.HTTP_204_NO_CONTENT)
@extract_user_id
async def upgrade_subscription(subscription_model: str, 
                                user_id: int = None,
                                token: int = Depends(oauth2_scheme),
                                db: Session = Depends(get_db)):
    service = PurchaseService(db)
    return service.upgrade_subscription(user_id, subscription_model)