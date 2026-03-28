from supabase import Client
from fastapi import HTTPException
from uuid import UUID
from backend.repositories.order import OrderRepository
from backend.schemas.order import OrderCreate, OrderUpdate


class OrderService:
    def __init__(self, client: Client):
        self.repo = OrderRepository(client)

    def get_order(self, order_id: UUID) -> dict:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def get_orders(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_order(self, order: OrderCreate) -> dict:
        return self.repo.create(order)

    def update_order(self, order_id: UUID, update_data: OrderUpdate) -> dict:
        self.get_order(order_id)  # Ensure exists
        return self.repo.update(order_id, update_data)

    def delete_order(self, order_id: UUID):
        self.get_order(order_id)  # Ensure exists
        self.repo.delete(order_id)
        return {"detail": "Order deleted successfully"}
