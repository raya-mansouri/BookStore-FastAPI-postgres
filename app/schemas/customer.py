from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class SubscriptionModel(str, Enum):
    free = "free"
    plus = "plus"
    premium = "premium"

class CustomerBase(BaseModel):
    user_id: int = Field(..., description="The ID of the user associated with the customer", example=1)
    subscription_model: str = Field(SubscriptionModel.free, description="Subscription model of the customer", example="free")
    subscription_end_time: Optional[datetime] = Field(None, description="End time of the subscription", example="2023-12-31T23:59:59")
    wallet_money_amount: int = Field(0, description="Amount of money in the wallet", example=10000)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    subscription_model: Optional[str] = Field(None, description="Subscription model of the customer", example="premium")
    subscription_end_time: Optional[datetime] = Field(None, description="End time of the subscription", example="2024-12-31T23:59:59")
    wallet_money_amount: Optional[int] = Field(None, description="Amount of money in the wallet", example=20000)

class CustomerOut(CustomerBase):
    id: int = Field(..., description="The unique identifier for the customer", example=1)

    class Config:
        orm_mode = True