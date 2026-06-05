from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from uuid import UUID
from typing import List

from database.session import get_supabase
from schemas.service_call import ServiceCallCreate, ServiceCallUpdate, ServiceCallResponse
from schemas.enums import ServiceStatus
from services.service_call import ServiceCallService
from api.deps import require_permissions, user_has_permission
from core.rbac import Permission

router = APIRouter(prefix="/service-calls", tags=["Service Calls"])

@router.post("/", response_model=ServiceCallResponse, status_code=status.HTTP_201_CREATED)
def create_service_call(
    service_call_in: ServiceCallCreate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(require_permissions(Permission.SERVICE_CALLS_WRITE))
):
    service = ServiceCallService(client)
    return service.create_service_call(service_call_in)

@router.get("/", response_model=List[ServiceCallResponse])
def get_service_calls(
    skip: int = 0,
    limit: int = 100,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(require_permissions(Permission.SERVICE_CALLS_READ))
):
    service = ServiceCallService(client)
    return service.get_service_calls(skip=skip, limit=limit)

@router.get("/{service_call_id}", response_model=ServiceCallResponse)
def get_service_call(
    service_call_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(require_permissions(Permission.SERVICE_CALLS_READ))
):
    service = ServiceCallService(client)
    return service.get_service_call(service_call_id)

@router.patch("/{service_call_id}", response_model=ServiceCallResponse)
def update_service_call(
    service_call_id: UUID,
    service_call_in: ServiceCallUpdate,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(require_permissions(Permission.SERVICE_CALLS_WRITE))
):
    if service_call_in.status in {ServiceStatus.resolved, ServiceStatus.closed} and not user_has_permission(
        current_user,
        Permission.SERVICE_CALLS_RESOLVE,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to resolve or close service calls.",
        )

    service = ServiceCallService(client)
    return service.update_service_call(service_call_id, service_call_in)

@router.delete("/{service_call_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_call(
    service_call_id: UUID,
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(require_permissions(Permission.SERVICE_CALLS_WRITE))
):
    service = ServiceCallService(client)
    service.delete_service_call(service_call_id)
