from pydantic import BaseModel
from typing import List

class DashboardSummary(BaseModel):
    open_service_calls_count: int
    machines_under_warranty_count: int
    machines_nearing_warranty_expiry_count: int
    machines_under_maintenance_count: int

class ReliabilityStat(BaseModel):
    model: str
    failure_count: int

class DashboardReliability(BaseModel):
    stats: List[ReliabilityStat]
