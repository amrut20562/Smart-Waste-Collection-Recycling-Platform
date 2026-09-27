from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from app.db import Base

class RouteRun(Base):
    __tablename__ = "route_runs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    solver_status = Column(String, nullable=False)
    estimated_total_distance_km = Column(Float, nullable=False)
    baseline_distance_km = Column(Float, nullable=False)
    estimated_distance_reduction_pct = Column(Float, nullable=False)
    vehicle_count = Column(Integer, nullable=False)

class RouteStop(Base):
    __tablename__ = "route_stops"

    id = Column(Integer, primary_key=True, index=True)
    route_run_id = Column(Integer, ForeignKey("route_runs.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    pickup_request_id = Column(Integer, ForeignKey("pickup_requests.id"), nullable=False)
    stop_order = Column(Integer, nullable=False)
    estimated_arrival_minutes = Column(Float, nullable=True)