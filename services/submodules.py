from supabase import Client
from fastapi import HTTPException
from uuid import UUID
from backend.repositories.submodules import SubmoduleRepository


class SubmoduleService:
    def __init__(self, client: Client, table_name: str):
        self.repo = SubmoduleRepository(client, table_name)

    def get_by_order(self, order_id: UUID) -> dict:
        obj = self.repo.get_by_order(order_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Submodule record not found for this order")
        return obj

    def create(self, create_schema) -> dict:
        # Check if exists first
        existing = self.repo.get_by_order(create_schema.order_id)
        if existing:
            raise HTTPException(status_code=400, detail="Record already exists for this order")
        return self.repo.create(create_schema)

    def update(self, order_id: UUID, update_data) -> dict:
        self.get_by_order(order_id)  # Ensure exists
        return self.repo.update(order_id, update_data)

    def delete(self, order_id: UUID):
        self.get_by_order(order_id)  # Ensure exists
        self.repo.delete(order_id)
        return {"detail": "Deleted successfully"}
