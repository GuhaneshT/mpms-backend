from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from backend.schemas.enums import OrderStatus

class OrderBase(BaseModel):
    customer_id: UUID
    status: Optional[OrderStatus] = OrderStatus.order_received

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderResponse(OrderBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
