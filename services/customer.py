from supabase import Client
from fastapi import HTTPException
from uuid import UUID
from repositories.customer import CustomerRepository
from schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, client: Client):
        self.repo = CustomerRepository(client)

    def get_customer(self, customer_id: UUID) -> dict:
        customer = self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    def get_customers(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_customer(self, customer: CustomerCreate) -> dict:
        return self.repo.create(customer)

    def update_customer(self, customer_id: UUID, update_data: CustomerUpdate) -> dict:
        self.get_customer(customer_id)  # Ensure exists
        return self.repo.update(customer_id, update_data)

    def delete_customer(self, customer_id: UUID):
        self.get_customer(customer_id)  # Ensure exists
        self.repo.delete(customer_id)
        return {"detail": "Customer deleted successfully"}
