from supabase import Client
from schemas.customer import CustomerCreate, CustomerUpdate, CustomerContactCreate
from uuid import UUID


class CustomerRepository:
    TABLE = "customers"

    def __init__(self, client: Client):
        self.client = client

    def get_by_id(self, customer_id: UUID) -> dict | None:
        response = (
            self.client.table(self.TABLE)
            .select("*, contacts:customer_contacts(*)")
            .eq("id", str(customer_id))
            .maybe_single()
            .execute()
        )
        return response.data

    def get_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        response = (
            self.client.table(self.TABLE)
            .select("*, contacts:customer_contacts(*)")
            .range(skip, skip + limit - 1)
            .execute()
        )
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


class CustomerContactRepository:
    TABLE = "customer_contacts"

    def __init__(self, client: Client):
        self.client = client

    def list_by_customer(self, customer_id: UUID) -> list[dict]:
        response = (
            self.client.table(self.TABLE)
            .select("*")
            .eq("customer_id", str(customer_id))
            .execute()
        )
        return response.data

    def create(self, customer_id: UUID, contact: CustomerContactCreate) -> dict:
        data = contact.model_dump(mode="json")
        data["customer_id"] = str(customer_id)
        response = self.client.table(self.TABLE).insert(data).execute()
        return response.data[0]

    def delete(self, contact_id: UUID):
        self.client.table(self.TABLE).delete().eq("id", str(contact_id)).execute()

