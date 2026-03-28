from fastapi import APIRouter, Depends, status
from supabase import Client
from uuid import UUID

from database.session import get_supabase
from api.deps import get_current_user
from repositories.submodules import SUBMODULE_TABLES
from schemas import submodules as schemas
from services.submodules import SubmoduleService

router = APIRouter(prefix="/orders", tags=["Order Submodules"])

# --- Production Chart ---
@router.post("/{order_id}/production-chart", response_model=schemas.ProductionChartResponse)
def create_production_chart(order_id: UUID, item_in: schemas.ProductionChartBase, client: Client = Depends(get_supabase)):
    create_dto = schemas.ProductionChartCreate(order_id=order_id, **item_in.model_dump())
    return SubmoduleService(client, SUBMODULE_TABLES["ProductionChart"]).create(create_dto)

@router.get("/{order_id}/production-chart", response_model=schemas.ProductionChartResponse)
def get_production_chart(order_id: UUID, client: Client = Depends(get_supabase)):
    return SubmoduleService(client, SUBMODULE_TABLES["ProductionChart"]).get_by_order(order_id)

# --- Ancillary Equipment ---
@router.post("/{order_id}/ancillary-equipment", response_model=schemas.AncillaryEquipmentResponse)
def create_ancillary_equipment(order_id: UUID, item_in: schemas.AncillaryEquipmentBase, client: Client = Depends(get_supabase)):
    create_dto = schemas.AncillaryEquipmentCreate(order_id=order_id, **item_in.model_dump())
    return SubmoduleService(client, SUBMODULE_TABLES["AncillaryEquipment"]).create(create_dto)

@router.get("/{order_id}/ancillary-equipment", response_model=schemas.AncillaryEquipmentResponse)
def get_ancillary_equipment(order_id: UUID, client: Client = Depends(get_supabase)):
    return SubmoduleService(client, SUBMODULE_TABLES["AncillaryEquipment"]).get_by_order(order_id)

# --- Site Verification ---
@router.post("/{order_id}/site-verification", response_model=schemas.SiteVerificationResponse)
def create_site_verification(order_id: UUID, item_in: schemas.SiteVerificationBase, client: Client = Depends(get_supabase)):
    create_dto = schemas.SiteVerificationCreate(order_id=order_id, **item_in.model_dump())
    return SubmoduleService(client, SUBMODULE_TABLES["SiteVerification"]).create(create_dto)

@router.get("/{order_id}/site-verification", response_model=schemas.SiteVerificationResponse)
def get_site_verification(order_id: UUID, client: Client = Depends(get_supabase)):
    return SubmoduleService(client, SUBMODULE_TABLES["SiteVerification"]).get_by_order(order_id)

# --- Packing List ---
@router.post("/{order_id}/packing-list", response_model=schemas.PackingListResponse)
def create_packing_list(order_id: UUID, item_in: schemas.PackingListBase, client: Client = Depends(get_supabase)):
    create_dto = schemas.PackingListCreate(order_id=order_id, **item_in.model_dump())
    return SubmoduleService(client, SUBMODULE_TABLES["PackingList"]).create(create_dto)

@router.get("/{order_id}/packing-list", response_model=schemas.PackingListResponse)
def get_packing_list(order_id: UUID, client: Client = Depends(get_supabase)):
    return SubmoduleService(client, SUBMODULE_TABLES["PackingList"]).get_by_order(order_id)

# --- Material Verification ---
@router.post("/{order_id}/material-verification", response_model=schemas.MaterialVerificationResponse)
def create_material_verification(order_id: UUID, item_in: schemas.MaterialVerificationBase, client: Client = Depends(get_supabase)):
    create_dto = schemas.MaterialVerificationCreate(order_id=order_id, **item_in.model_dump())
    return SubmoduleService(client, SUBMODULE_TABLES["MaterialVerification"]).create(create_dto)

@router.get("/{order_id}/material-verification", response_model=schemas.MaterialVerificationResponse)
def get_material_verification(order_id: UUID, client: Client = Depends(get_supabase)):
    return SubmoduleService(client, SUBMODULE_TABLES["MaterialVerification"]).get_by_order(order_id)

# --- Installation Record ---
@router.post("/{order_id}/installation-record", response_model=schemas.InstallationRecordResponse)
def create_installation_record(order_id: UUID, item_in: schemas.InstallationRecordBase, client: Client = Depends(get_supabase)):
    create_dto = schemas.InstallationRecordCreate(order_id=order_id, **item_in.model_dump())
    return SubmoduleService(client, SUBMODULE_TABLES["InstallationRecord"]).create(create_dto)

@router.get("/{order_id}/installation-record", response_model=schemas.InstallationRecordResponse)
def get_installation_record(order_id: UUID, client: Client = Depends(get_supabase)):
    return SubmoduleService(client, SUBMODULE_TABLES["InstallationRecord"]).get_by_order(order_id)
