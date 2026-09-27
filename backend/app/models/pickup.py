from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, func
from app.db import Base
import enum

class PickupStatus(str, enum.Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class PickupRequest(Base):
    __tablename__ = "pickup_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    waste_category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    scheduled_date = Column(String, nullable=False) # e.g. YYYY-MM-DD
    scheduled_window = Column(String, nullable=True)
    load_units = Column(Integer, default=1)
    priority_score = Column(Float, default=0.0)
    priority_reasons_json = Column(String, nullable=True)
    status = Column(Enum(PickupStatus), default=PickupStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())