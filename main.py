from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from alembic import command
from alembic.config import Config
from app.api.dependency import http_exception_handler, validation_exception_handler
from fastapi.exceptions import HTTPException, RequestValidationError
# Import routers
from app.api.auth_api import router as auth_router
from app.api.book_api import router as book_router
from app.api.user_api import router as user_router
from app.api.customer_api import router as customer_router
# from app.api.reservation_api import router as reservation_router
# from app.api.purchase_api import router as purchase_router

# Import database setup
from app.models.base import Base, engine, SessionLocal

# Import services (if needed for dependencies)
# from app.services.auth_service import get_current_user

# Initialize FastAPI app
app = FastAPI(
    title="Book Store API",
    description="A simple CRUD system for managing books, users, customers, and reservations.",
    version="1.0.0",
)

# Register custom exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(book_router, prefix="/books", tags=["Books"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])
# app.include_router(reservation_router, prefix="/reservations", tags=["Reservations"])
# app.include_router(purchase_router, prefix="/purchases", tags=["Purchases"])

# Database dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Run database migrations on startup
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

# Run migrations when the app starts
# @app.on_event("startup")
# def on_startup():
#     run_migrations()

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the Book Store API!"}

# Example of a protected endpoint
# @app.get("/protected", tags=["Test"])
# def protected_route(current_user: dict = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user['username']}! This is a protected route."}