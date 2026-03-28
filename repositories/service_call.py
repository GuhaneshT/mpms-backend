from supabase import Client
from backend.schemas.service_call import ServiceCallCreate, ServiceCallUpdate
from uuid import UUID


class ServiceCallRepository:
    TABLE = "service_calls"

    def __init__(self, client: Client):
        self.client = client

    def get_by_id(self, service_call_id: UUID) -> dict | None:
        response = self.client.table(self.TABLE).select("*").eq("id", str(service_call_id)).maybe_single().execute()
        return response.data

    def get_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        response = (
            self.client.table(self.TABLE)
            .select("*")
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return response.data

    def get_by_machine(self, machine_id: UUID) -> list[dict]:
        response = self.client.table(self.TABLE).select("*").eq("machine_id", str(machine_id)).execute()
        return response.data

    def create(self, service_call: ServiceCallCreate) -> dict:
        data = service_call.model_dump(mode="json")
        # Convert enums to string values for Supabase
        for field in ["department", "status"]:
            if field in data and data[field] is not None:
                data[field] = data[field] if isinstance(data[field], str) else data[field].value
        response = self.client.table(self.TABLE).insert(data).execute()
        return response.data[0]

    def update(self, service_call_id: UUID, update_data: ServiceCallUpdate) -> dict:
        update_dict = update_data.model_dump(exclude_unset=True, mode="json")
        for field in ["department", "status"]:
            if field in update_dict and update_dict[field] is not None:
                update_dict[field] = update_dict[field] if isinstance(update_dict[field], str) else update_dict[field].value
        response = self.client.table(self.TABLE).update(update_dict).eq("id", str(service_call_id)).execute()
        return response.data[0]

    def delete(self, service_call_id: UUID):
        self.client.table(self.TABLE).delete().eq("id", str(service_call_id)).execute()
