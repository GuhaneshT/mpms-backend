from fastapi import APIRouter, Depends, status
from supabase import Client
from uuid import UUID
from typing import List

from backend.database.session import get_supabase
from backend.schemas.service_call import ServiceCallCreate, ServiceCallUpdate, ServiceCallResponse
from backend.services.service_call import ServiceCallService
from backend.api.deps import get_current_user

router = APIRouter(prefix="/service-calls", tags=["Service Calls"])

@router.post("/", response_model=ServiceCallResponse, status_code=status.HTTP_201_CREATED)
def create_service_call(
    service_call_in: ServiceCallCreate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = ServiceCallService(client)
    return service.create_service_call(service_call_in)

@router.get("/", response_model=List[ServiceCallResponse])
def get_service_calls(
    skip: int = 0,
    limit: int = 100,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = ServiceCallService(client)
    return service.get_service_calls(skip=skip, limit=limit)

@router.get("/{service_call_id}", response_model=ServiceCallResponse)
def get_service_call(
    service_call_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = ServiceCallService(client)
    return service.get_service_call(service_call_id)

@router.patch("/{service_call_id}", response_model=ServiceCallResponse)
def update_service_call(
    service_call_id: UUID,
    service_call_in: ServiceCallUpdate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = ServiceCallService(client)
    return service.update_service_call(service_call_id, service_call_in)

@router.delete("/{service_call_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_call(
    service_call_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    service = ServiceCallService(client)
    service.delete_service_call(service_call_id)
