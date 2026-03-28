from fastapi import APIRouter, Depends, status
from supabase import Client
from uuid import UUID
from typing import List

from database.session import get_supabase
from schemas.order import OrderCreate, OrderUpdate, OrderResponse
from services.order import OrderService
from api.deps import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = OrderService(client)
    return service.create_order(order_in)

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = OrderService(client)
    return service.get_orders(skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = OrderService(client)
    return service.get_order(order_id)

@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: UUID,
    order_in: OrderUpdate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = OrderService(client)
    return service.update_order(order_id, order_in)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = OrderService(client)
    service.delete_order(order_id)
