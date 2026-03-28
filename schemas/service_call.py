from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime
from backend.schemas.enums import ServiceDepartment, ServiceStatus

class ServiceCallBase(BaseModel):
    machine_id: UUID
    is_warranty: Optional[bool] = False
    department: ServiceDepartment
    error_description: str
    solution: Optional[str] = None
    parts_used: Optional[Any] = None
    status: Optional[ServiceStatus] = ServiceStatus.open
    technician_id: Optional[UUID] = None

class ServiceCallCreate(ServiceCallBase):
    pass

class ServiceCallUpdate(BaseModel):
    is_warranty: Optional[bool] = None
    department: Optional[ServiceDepartment] = None
    error_description: Optional[str] = None
    solution: Optional[str] = None
    parts_used: Optional[Any] = None
    status: Optional[ServiceStatus] = None
    technician_id: Optional[UUID] = None

class ServiceCallResponse(ServiceCallBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
