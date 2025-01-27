from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut
from app.services.customer_service import CustomerService
from app.dependency import get_db

router = APIRouter()

@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.create_customer(customer_data)

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_customer(customer_id)

@router.get("/", response_model=List[CustomerOut])
def get_all_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_all_customers(skip=skip, limit=limit)

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.update_customer(customer_id, customer_data)

@router.patch("/{customer_id}", response_model=CustomerOut)
def patch_customer(customer_id: int, update_data: dict, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.patch_customer(customer_id, update_data)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    service.delete_customer(customer_id)
    return None