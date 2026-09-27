from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.pickup import PickupStatus

class PickupCreate(BaseModel):
    user_id: int
    waste_category: str
    latitude: float
    longitude: float
    scheduled_date: str
    scheduled_window: Optional[str] = None
    load_units: int = 1
    description: Optional[str] = None

class PickupStatusUpdate(BaseModel):
    status: PickupStatus

class PickupResponse(BaseModel):
    id: int
    user_id: int
    waste_category: str
    description: Optional[str]
    latitude: float
    longitude: float
    scheduled_date: str
    scheduled_window: Optional[str]
    load_units: int
    priority_score: float
    priority_reasons_json: Optional[str]
    status: PickupStatus
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
