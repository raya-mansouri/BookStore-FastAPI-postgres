from sqlalchemy.orm import Session

from app.models.customer import Customer

class PurchaseService:
    def __init__(self, db: Session):
        self.db = db

    def charge_wallet(self, customer_id: int, amount: int) -> Customer:
        customer = self.db.query(Customer).get(customer_id)
        customer.wallet_money_amount += amount
        self.db.commit()
        return customer

    def upgrade_subscription(self, customer_id: int, subscription_model: str) -> Customer:
        customer = self.db.query(Customer).get(customer_id)
        # Deduct cost from wallet (e.g., 50,000 Toman for "plus")
        customer.subscription_model = subscription_model
        self.db.commit()
        return customer