from supabase import Client
from fastapi import HTTPException
from uuid import UUID
from repositories.machine import MachineRepository
from schemas.machine import MachineCreate, MachineUpdate


class MachineService:
    def __init__(self, client: Client):
        self.repo = MachineRepository(client)

    def get_machine(self, machine_id: UUID) -> dict:
        machine = self.repo.get_by_id(machine_id)
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        return machine

    def get_machines(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_machine(self, machine: MachineCreate) -> dict:
        return self.repo.create(machine)

    def update_machine(self, machine_id: UUID, update_data: MachineUpdate) -> dict:
        self.get_machine(machine_id)  # Ensure exists
        return self.repo.update(machine_id, update_data)

    def delete_machine(self, machine_id: UUID):
        self.get_machine(machine_id)  # Ensure exists
        self.repo.delete(machine_id)
        return {"detail": "Machine deleted successfully"}
