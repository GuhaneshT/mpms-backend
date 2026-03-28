from supabase import Client
from backend.schemas.machine import MachineCreate, MachineUpdate
from uuid import UUID


class MachineRepository:
    TABLE = "machines"

    def __init__(self, client: Client):
        self.client = client

    def get_by_id(self, machine_id: UUID) -> dict | None:
        response = self.client.table(self.TABLE).select("*").eq("id", str(machine_id)).maybe_single().execute()
        return response.data

    def get_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        response = self.client.table(self.TABLE).select("*").range(skip, skip + limit - 1).execute()
        return response.data

    def create(self, machine: MachineCreate) -> dict:
        data = machine.model_dump(mode="json")
        if "status" in data and data["status"] is not None:
            data["status"] = data["status"] if isinstance(data["status"], str) else data["status"].value
        response = self.client.table(self.TABLE).insert(data).execute()
        return response.data[0]

    def update(self, machine_id: UUID, update_data: MachineUpdate) -> dict:
        update_dict = update_data.model_dump(exclude_unset=True, mode="json")
        if "status" in update_dict and update_dict["status"] is not None:
            update_dict["status"] = update_dict["status"] if isinstance(update_dict["status"], str) else update_dict["status"].value
        response = self.client.table(self.TABLE).update(update_dict).eq("id", str(machine_id)).execute()
        return response.data[0]

    def delete(self, machine_id: UUID):
        self.client.table(self.TABLE).delete().eq("id", str(machine_id)).execute()
