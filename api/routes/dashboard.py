from fastapi import APIRouter, Depends
from supabase import Client
from datetime import datetime, timedelta, timezone

from backend.database.session import get_supabase
from backend.api.deps import get_current_user
from backend.schemas.dashboard import DashboardSummary, DashboardReliability, ReliabilityStat

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    now = datetime.now(timezone.utc).isoformat()
    thirty_days_from_now = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()

    # Open service calls (status is 'open' or 'in_progress')
    open_calls = client.table("service_calls").select("id", count="exact").in_(
        "status", ["open", "in_progress"]
    ).execute()
    open_service_calls = open_calls.count or 0

    # Machines under warranty (warranty_end >= now)
    warranty_result = client.table("machines").select("id", count="exact").gte(
        "warranty_end", now
    ).execute()
    machines_under_warranty = warranty_result.count or 0

    # Machines nearing warranty expiry (warranty_end >= now AND warranty_end <= 30 days from now)
    nearing_result = client.table("machines").select("id", count="exact").gte(
        "warranty_end", now
    ).lte(
        "warranty_end", thirty_days_from_now
    ).execute()
    machines_nearing_expiry = nearing_result.count or 0

    # Machines under maintenance
    maintenance_result = client.table("machines").select("id", count="exact").eq(
        "status", "under_maintenance"
    ).execute()
    machines_under_maintenance = maintenance_result.count or 0

    return DashboardSummary(
        open_service_calls_count=open_service_calls,
        machines_under_warranty_count=machines_under_warranty,
        machines_nearing_warranty_expiry_count=machines_nearing_expiry,
        machines_under_maintenance_count=machines_under_maintenance
    )

@router.get("/reliability", response_model=DashboardReliability)
def get_machine_reliability(
    client: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user)
):
    """
    Get machine reliability stats: failure counts grouped by model.
    A failure is an open/in_progress service call.
    """
    # This is a simplified aggregation of open/in-progress calls grouped by linked machine model
    calls_res = client.table("service_calls").select("id, status, machines(model)").in_(
        "status", ["open", "in_progress"]
    ).execute()
    
    counts = {}
    for call in (calls_res.data or []):
        model = call.get("machines", {}).get("model", "Unknown")
        counts[model] = counts.get(model, 0) + 1
    
    stats = [ReliabilityStat(model=m, failure_count=c) for m, c in counts.items()]
    return DashboardReliability(stats=stats)
