from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# ── Customer Contact ──────────────────────────────────────────────────────────

class CustomerContactBase(BaseModel):
    name: str
    phone: Optional[str] = None
    designation: Optional[str] = None

class CustomerContactCreate(CustomerContactBase):
    pass

class CustomerContactResponse(CustomerContactBase):
    id: UUID
    customer_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Customer ──────────────────────────────────────────────────────────────────

class CustomerBase(BaseModel):
    name: str
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    gst: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: UUID
    contacts: List[CustomerContactResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

