from fastapi import APIRouter, Depends, status
from supabase import Client
from uuid import UUID
from typing import List

from backend.database.session import get_supabase
from backend.schemas.machine import MachineCreate, MachineUpdate, MachineResponse
from backend.services.machine import MachineService
from backend.api.deps import get_current_user

router = APIRouter(prefix="/machines", tags=["Machines"])

@router.post("/", response_model=MachineResponse, status_code=status.HTTP_201_CREATED)
def create_machine(
    machine_in: MachineCreate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = MachineService(client)
    return service.create_machine(machine_in)

@router.get("/", response_model=List[MachineResponse])
def get_machines(
    skip: int = 0,
    limit: int = 100,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = MachineService(client)
    return service.get_machines(skip=skip, limit=limit)

@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(
    machine_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = MachineService(client)
    return service.get_machine(machine_id)

@router.patch("/{machine_id}", response_model=MachineResponse)
def update_machine(
    machine_id: UUID,
    machine_in: MachineUpdate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = MachineService(client)
    return service.update_machine(machine_id, machine_in)

@router.delete("/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_machine(
    machine_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = MachineService(client)
    service.delete_machine(machine_id)
