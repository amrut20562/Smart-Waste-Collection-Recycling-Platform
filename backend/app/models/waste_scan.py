from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db import Base

class WasteScan(Base):
    __tablename__ = "waste_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    image_path = Column(String, nullable=True)
    primary_category = Column(String, nullable=False)
    source = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    detections_json = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())