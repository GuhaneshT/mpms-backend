from pydantic import BaseModel
from typing import Optional, Any, List
from uuid import UUID
from datetime import datetime
from backend.schemas.enums import SiteVerificationStatus

# Production Chart
class ProductionChartBase(BaseModel):
    notes: Optional[str] = None
    chart_data: Optional[Any] = None

class ProductionChartCreate(ProductionChartBase):
    order_id: UUID

class ProductionChartUpdate(ProductionChartBase):
    pass

class ProductionChartResponse(ProductionChartBase):
    id: UUID
    order_id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

# Ancillary Equipment
class AncillaryEquipmentBase(BaseModel):
    items: Any
    notes: Optional[str] = None

class AncillaryEquipmentCreate(AncillaryEquipmentBase):
    order_id: UUID

class AncillaryEquipmentUpdate(AncillaryEquipmentBase):
    pass

class AncillaryEquipmentResponse(AncillaryEquipmentBase):
    id: UUID
    order_id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

# Site Verification
class SiteVerificationBase(BaseModel):
    layout_notes: Optional[str] = None
    floor_dimensions: Optional[str] = None
    power_specs: Optional[str] = None
    status: Optional[SiteVerificationStatus] = SiteVerificationStatus.pending

class SiteVerificationCreate(SiteVerificationBase):
    order_id: UUID

class SiteVerificationUpdate(SiteVerificationBase):
    pass

class SiteVerificationResponse(SiteVerificationBase):
    id: UUID
    order_id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

# Packing List
class PackingListBase(BaseModel):
    accessories: Optional[Any] = None
    notes: Optional[str] = None

class PackingListCreate(PackingListBase):
    order_id: UUID

class PackingListUpdate(PackingListBase):
    pass

class PackingListResponse(PackingListBase):
    id: UUID
    order_id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}

# Material Verification
class MaterialVerificationBase(BaseModel):
    is_verified: Optional[bool] = False
    notes: Optional[str] = None

class MaterialVerificationCreate(MaterialVerificationBase):
    order_id: UUID

class MaterialVerificationUpdate(MaterialVerificationBase):
    verified_at: Optional[datetime] = None

class MaterialVerificationResponse(MaterialVerificationBase):
    id: UUID
    order_id: UUID
    verified_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

# Installation Record
class InstallationRecordBase(BaseModel):
    installed_by: Optional[str] = None
    notes: Optional[str] = None

class InstallationRecordCreate(InstallationRecordBase):
    order_id: UUID

class InstallationRecordUpdate(InstallationRecordBase):
    pass

class InstallationRecordResponse(InstallationRecordBase):
    id: UUID
    order_id: UUID
    installation_date: datetime
    model_config = {"from_attributes": True}
