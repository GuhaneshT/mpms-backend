from supabase import Client
from fastapi import HTTPException
from uuid import UUID
from backend.repositories.service_call import ServiceCallRepository
from backend.schemas.service_call import ServiceCallCreate, ServiceCallUpdate


class ServiceCallService:
    def __init__(self, client: Client):
        self.repo = ServiceCallRepository(client)

    def get_service_call(self, service_call_id: UUID) -> dict:
        service_call = self.repo.get_by_id(service_call_id)
        if not service_call:
            raise HTTPException(status_code=404, detail="Service call not found")
        return service_call

    def get_service_calls(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_service_call(self, service_call: ServiceCallCreate) -> dict:
        return self.repo.create(service_call)

    def update_service_call(self, service_call_id: UUID, update_data: ServiceCallUpdate) -> dict:
        self.get_service_call(service_call_id)  # Ensure exists
        return self.repo.update(service_call_id, update_data)

    def delete_service_call(self, service_call_id: UUID):
        self.get_service_call(service_call_id)  # Ensure exists
        self.repo.delete(service_call_id)
        return {"detail": "Service call deleted successfully"}
