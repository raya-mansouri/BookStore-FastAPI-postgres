from sqlalchemy.orm import Session
from sqlalchemy import event
from app.models.base import SessionLocal
from app.models import User, Customer, Author

@event.listens_for(User, "after_insert")
def create_related_record(mapper, connection, target):
    session = Session(bind=connection)

    if target.role == "customer":
        entity = Customer(
            user_id=target.id,
            subscription_model="free",
            subscription_end_time=None,
            wallet_money_amount=0
        )
    elif target.role == "author":
        entity = Author(
            user_id=target.id,
            biography="",
            books_published=0
        )
    else:
        return

    session.add(entity)
    session.commit()
    session.close()

#https://chatgpt.com/share/67a74a01-1054-8005-99bb-59d2242bbcb1