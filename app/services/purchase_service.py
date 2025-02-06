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
        customer.charge_wallet(amount)
        self.db.commit()
        return customer

    def upgrade_subscription(self, user_id: int, subscription_model: str) -> Customer:
        customer = self.db.query(Customer).filter(Customer.user_id == user_id).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        customer.upgrade_subscription(subscription_model)
        self.db.commit()
        return customer