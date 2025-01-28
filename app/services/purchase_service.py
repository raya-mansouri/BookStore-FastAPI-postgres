from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.customer import Customer

class PurchaseService:
    def __init__(self, db: Session):
        self.db = db

    def charge_wallet(self, user_id: int, amount: int) -> Customer:
        customer = self.db.query(Customer).filter(Customer.user_id == user_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        customer.wallet_money_amount += amount
        self.db.commit()
        return customer

    def upgrade_subscription(self, user_id: int, subscription_model: str) -> Customer:
        customer = self.db.query(Customer).filter(Customer.user_id == user_id).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        pre_wallet_amount = customer.wallet_money_amount
        if subscription_model == "plus":
            cost = 50000
        else:
            pre_subscription_model = customer.subscription_model
            if pre_subscription_model == "plus":
                cost = 150000
            else:
                cost = 200000

        if pre_wallet_amount < cost:
            raise HTTPException(status_code=400, detail="Insufficient wallet balance")
        
        customer.wallet_money_amount -= cost
        customer.subscription_model = subscription_model
        self.db.commit()
        return customer