from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from schemas.enums import MachineStatus

class MachineBase(BaseModel):
    order_id: UUID
    serial_number: str
    model: str
    vendor: Optional[str] = None
    installation_date: Optional[datetime] = None
    warranty_start: Optional[datetime] = None
    warranty_end: Optional[datetime] = None
    status: Optional[MachineStatus] = MachineStatus.in_transit

class MachineCreate(MachineBase):
    pass

class MachineUpdate(BaseModel):
    status: Optional[MachineStatus] = None
    installation_date: Optional[datetime] = None
    warranty_start: Optional[datetime] = None
    warranty_end: Optional[datetime] = None

class MachineResponse(MachineBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
