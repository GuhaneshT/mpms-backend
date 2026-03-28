from supabase import Client
from backend.schemas.customer import CustomerCreate, CustomerUpdate
from uuid import UUID


class CustomerRepository:
    TABLE = "customers"

    def __init__(self, client: Client):
        self.client = client

    def get_by_id(self, customer_id: UUID) -> dict | None:
        response = self.client.table(self.TABLE).select("*").eq("id", str(customer_id)).maybe_single().execute()
        return response.data

    def get_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        response = self.client.table(self.TABLE).select("*").range(skip, skip + limit - 1).execute()
        return response.data

    def create(self, customer: CustomerCreate) -> dict:
        response = self.client.table(self.TABLE).insert(customer.model_dump(mode="json")).execute()
        return response.data[0]

    def update(self, customer_id: UUID, update_data: CustomerUpdate) -> dict:
        update_dict = update_data.model_dump(exclude_unset=True, mode="json")
        response = self.client.table(self.TABLE).update(update_dict).eq("id", str(customer_id)).execute()
        return response.data[0]

    def delete(self, customer_id: UUID):
        self.client.table(self.TABLE).delete().eq("id", str(customer_id)).execute()
