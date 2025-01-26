from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from app.models.user import User
from app.models.author import Author
from app.models.customer import Customer
from app.models.book import Book
from app.models.reservation import Reservation
from app.models.city import City
from app.models.genre import Genre
from app.models.book_author import BookAuthor
from sqlalchemy.orm import Session
from app.models.base import SessionLocal


import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a configured Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()
session = SessionLocal()


# users = [
#     User(
#         username="john_doe",
#         first_name="John",
#         last_name="Doe",
#         phone="09123456789",
#         email="john.doe@example.com",
#         password="password123",
#         role="customer"
#     ),
#     User(
#         username="jane_smith",
#         first_name="Jane",
#         last_name="Smith",
#         phone="09234567890",
#         email="jane.smith@example.com",
#         password="password123",
#         role="author"
#     ),
#     User(
#         username="admin_user",
#         first_name="Admin",
#         last_name="User",
#         phone="09345678901",
#         email="admin.user@example.com",
#         password="admin123",
#         role="admin"
#     ),
#     User(
#         username="alice_wonder",
#         first_name="Alice",
#         last_name="Wonder",
#         phone="09456789012",
#         email="alice.wonder@example.com",
#         password="password123",
#         role="customer"
#     ),
#     User(
#         username="bob_builder",
#         first_name="Bob",
#         last_name="Builder",
#         phone="09567890123",
#         email="bob.builder@example.com",
#         password="password123",
#         role="author"
#     )
# ]

# session.add_all(users)
# session.commit()

#-------------------------------------
# cities = [
#     City(name="New York"),
#     City(name="Los Angeles"),
#     City(name="Chicago"),
#     City(name="Houston"),
#     City(name="Phoenix")
# ]

# session.add_all(cities)
# session.commit()
# #-------------------
# authors = [
#     Author(
#         user_id=2,  # jane_smith
#         city_id=1,  # New York
#         goodreads_link="https://www.goodreads.com/jane_smith",
#         bank_account_number="1234567890"
#     ),
#     Author(
#         user_id=5,  # bob_builder
#         city_id=2,  # Los Angeles
#         goodreads_link="https://www.goodreads.com/bob_builder",
#         bank_account_number="0987654321"
#     ),
#     Author(
#         user_id=1,  # john_doe
#         city_id=3,  # Chicago
#         goodreads_link="https://www.goodreads.com/john_doe",
#         bank_account_number="1122334455"
#     ),
#     Author(
#         user_id=4,  # alice_wonder
#         city_id=4,  # Houston
#         goodreads_link="https://www.goodreads.com/alice_wonder",
#         bank_account_number="5566778899"
#     ),
#     Author(
#         user_id=3,  # admin_user
#         city_id=5,  # Phoenix
#         goodreads_link="https://www.goodreads.com/admin_user",
#         bank_account_number="9988776655"
#     )
# ]

# session.add_all(authors)
# session.commit()

# # ---------------------

# genres = [
#     Genre(name="Science Fiction"),
#     Genre(name="Mystery"),
#     Genre(name="Romance"),
#     Genre(name="Fantasy"),
#     Genre(name="Thriller")
# ]

# session.add_all(genres)
# session.commit()
# #---------------------

# books = [
#     Book(
#         title="The Martian",
#         isbn="9780804139021",
#         price=15,
#         genre_id=1,  # Science Fiction
#         description="A man is stranded on Mars.",
#         units=10,
#         reserved_units=0,
#         authors=[authors[0], authors[4]]  # jane_smith
#     ),
#     Book(
#         title="Gone Girl",
#         isbn="9780307588371",
#         price=12,
#         genre_id=2,  # Mystery
#         description="A woman goes missing.",
#         units=8,
#         reserved_units=0,
#         authors=[authors[1]]  # bob_builder
#     ),
#     Book(
#         title="Pride and Prejudice",
#         isbn="9780141439518",
#         price=10,
#         genre_id=3,  # Romance
#         description="A classic love story.",
#         units=15,
#         reserved_units=0,
#         authors=[authors[2], authors[1]]  # john_doe
#     ),
#     Book(
#         title="The Hobbit",
#         isbn="9780547928227",
#         price=20,
#         genre_id=4,  # Fantasy
#         description="A hobbit's adventure.",
#         units=12,
#         reserved_units=0,
#         authors=[authors[3]]  # alice_wonder
#     ),
#     Book(
#         title="The Girl with the Dragon Tattoo",
#         isbn="9780307949486",
#         price=14,
#         genre_id=5,  # Thriller
#         description="A journalist investigates a disappearance.",
#         units=7,
#         reserved_units=0,
#         authors=[authors[4]]  # admin_user
#     )
# ]

# # Add books to the session
# session.add_all(books)
# session.commit()

# #-------------------------------


# customers = [
#     Customer(
#         user_id=1,  # john_doe
#         subscription_model="free",
#         subscription_end_time=None,
#         wallet_money_amount=50000
#     ),
#     Customer(
#         user_id=4,  # alice_wonder
#         subscription_model="premium",
#         subscription_end_time=datetime(2024, 12, 31),
#         wallet_money_amount=100000
#     ),
#     Customer(
#         user_id=3,  # admin_user
#         subscription_model="plus",
#         subscription_end_time=datetime(2024, 6, 30),
#         wallet_money_amount=75000
#     ),
#     Customer(
#         user_id=5,  # bob_builder
#         subscription_model="free",
#         subscription_end_time=None,
#         wallet_money_amount=25000
#     ),
#     Customer(
#         user_id=2,  # jane_smith
#         subscription_model="premium",
#         subscription_end_time=datetime(2024, 12, 31),
#         wallet_money_amount=150000
#     )
# ]

# session.add_all(customers)
# session.commit()
# #---------------------------

# from datetime import datetime, timedelta

# reservations = [
#     Reservation(
#         customer_id=1,  # john_doe
#         book_id=1,      # The Martian
#         start_of_reservation=datetime.now(),
#         end_of_reservation=datetime.now() + timedelta(days=7),
#         price=15.00,
#         status="active",
#         queue_position=1
#     ),
#     Reservation(
#         customer_id=2,  # alice_wonder
#         book_id=2,      # Gone Girl
#         start_of_reservation=datetime.now(),
#         end_of_reservation=datetime.now() + timedelta(days=7),
#         price=12.00,
#         status="pending",
#         queue_position=2
#     ),
#     Reservation(
#         customer_id=3,  # admin_user
#         book_id=3,      # Pride and Prejudice
#         start_of_reservation=datetime.now(),
#         end_of_reservation=datetime.now() + timedelta(days=7),
#         price=10.00,
#         status="completed",
#         queue_position=None
#     ),
#     Reservation(
#         customer_id=4,  # bob_builder
#         book_id=4,      # The Hobbit
#         start_of_reservation=datetime.now(),
#         end_of_reservation=datetime.now() + timedelta(days=7),
#         price=20.00,
#         status="active",
#         queue_position=1
#     ),
#     Reservation(
#         customer_id=5,  # jane_smith
#         book_id=5,      # The Girl with the Dragon Tattoo
#         start_of_reservation=datetime.now(),
#         end_of_reservation=datetime.now() + timedelta(days=7),
#         price=14.00,
#         status="pending",
#         queue_position=3
#     )
# ]

# session.add_all(reservations)
# session.commit()

# #-----------------------

# session.close()

existing_users = session.query(Customer).all()
for b in existing_users:
    print(b.id)