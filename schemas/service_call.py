from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime
from schemas.enums import ServiceDepartment, ServiceStatus

class ServiceCallBase(BaseModel):
    machine_id: UUID

    # New fields for service call report
    customer_name: Optional[str] = None
    visit_date: Optional[datetime] = None
    purpose_of_visit: Optional[str] = None
    machine_reference: Optional[Any] = None  # Expected list of dicts
    observation: Optional[str] = None
    corrective_measures: Optional[str] = None
    remarks: Optional[str] = None
    service_engg_name: Optional[str] = None
    to_be_attended_on: Optional[datetime] = None
    attended_on: Optional[datetime] = None

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
    # New fields
    customer_name: Optional[str] = None
    visit_date: Optional[datetime] = None
    purpose_of_visit: Optional[str] = None
    machine_reference: Optional[Any] = None
    observation: Optional[str] = None
    corrective_measures: Optional[str] = None
    remarks: Optional[str] = None
    service_engg_name: Optional[str] = None
    to_be_attended_on: Optional[datetime] = None
    attended_on: Optional[datetime] = None

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
