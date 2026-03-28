from fastapi import APIRouter, Depends, status
from supabase import Client
from uuid import UUID
from typing import List

from database.session import get_supabase
from schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from services.customer import CustomerService
from api.deps import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_in: CustomerCreate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = CustomerService(client)
    return service.create_customer(customer_in)

@router.get("/", response_model=List[CustomerResponse])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = CustomerService(client)
    return service.get_customers(skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = CustomerService(client)
    return service.get_customer(customer_id)

@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: UUID,
    customer_in: CustomerUpdate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = CustomerService(client)
    return service.update_customer(customer_id, customer_in)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = CustomerService(client)
    service.delete_customer(customer_id)
