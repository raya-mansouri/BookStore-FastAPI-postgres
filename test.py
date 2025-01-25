from app.models.customer import Customer
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.base import SessionLocal


db = SessionLocal()
# user = User(
#     username="john_doe",
#     first_name="John",
#     last_name="Doe",
#     phone="1234567890",
#     email="john.doe@example.com",
#     password="hashed_password",
#     role="customer"
# )
# db.add(user)
# db.commit()


# author = Author(
#     user_id=1,  # Assuming the user with ID 1 exists
#     city="New York",
#     goodreads_link="https://www.goodreads.com/john_doe",
#     bank_account_number="1234567890"
# )
# db.add(author)
# db.commit()

# customer = Customer(
#     user_id=1,
#     subscription_model="free",
#     wallet_money_amount=100.0
# )
# db.add(customer)
# db.commit()

# book = Book(
#     title="Sample Book",
#     isbn="978-3-16-148410-0",
#     price=29.99,
#     genre="Fiction",
#     description="A sample book description.",
#     units=10,
#     author_id=1  # Assuming the author with ID 1 exists
# )
# db.add(book)
# db.commit()

fetched_user = db.query(User).filter(User.username == "john_doe").first()
print(f"User: {fetched_user.username}")