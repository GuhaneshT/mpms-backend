from supabase import Client
from backend.schemas.order import OrderCreate, OrderUpdate
from uuid import UUID


class OrderRepository:
    TABLE = "orders"

    def __init__(self, client: Client):
        self.client = client

    def get_by_id(self, order_id: UUID) -> dict | None:
        response = self.client.table(self.TABLE).select("*").eq("id", str(order_id)).maybe_single().execute()
        return response.data

    def get_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        response = self.client.table(self.TABLE).select("*").range(skip, skip + limit - 1).execute()
        return response.data

    def get_by_customer(self, customer_id: UUID) -> list[dict]:
        response = self.client.table(self.TABLE).select("*").eq("customer_id", str(customer_id)).execute()
        return response.data

    def create(self, order: OrderCreate) -> dict:
        data = order.model_dump(mode="json")
        # Convert enum to its value for Supabase
        if "status" in data and data["status"] is not None:
            data["status"] = data["status"] if isinstance(data["status"], str) else data["status"].value
        response = self.client.table(self.TABLE).insert(data).execute()
        return response.data[0]

    def update(self, order_id: UUID, update_data: OrderUpdate) -> dict:
        update_dict = update_data.model_dump(exclude_unset=True, mode="json")
        if "status" in update_dict and update_dict["status"] is not None:
            update_dict["status"] = update_dict["status"] if isinstance(update_dict["status"], str) else update_dict["status"].value
        response = self.client.table(self.TABLE).update(update_dict).eq("id", str(order_id)).execute()
        return response.data[0]

    def delete(self, order_id: UUID):
        self.client.table(self.TABLE).delete().eq("id", str(order_id)).execute()
