from sqlalchemy import Column, Integer, String, Boolean, Float
from app.db import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capacity_units = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    start_latitude = Column(Float, nullable=False)
    start_longitude = Column(Float, nullable=False)