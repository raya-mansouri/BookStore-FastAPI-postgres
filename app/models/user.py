from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(11), nullable=False)  # 11 digits, starting with 09
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "customer", "author", name="user_roles"), nullable=False)
    subscription_end_time = Column(DateTime, nullable=True)
    # wallet_money_amount = Column(Integer, default=0, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    author = relationship("Author", back_populates="user", uselist=False, cascade="all, delete-orphan")
    customer = relationship("Customer", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password: str):
        """Hashes the password and stores it in the `password` column."""
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifies the provided password against the hashed password."""
        return pwd_context.verify(password, self.password)