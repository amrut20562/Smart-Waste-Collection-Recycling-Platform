from pydantic import BaseModel
from typing import List, Optional

class RouteOptimizeRequest(BaseModel):
    vehicle_ids: List[int]
    pickup_request_ids: List[int]

class VehicleRoute(BaseModel):
    vehicle_id: int
    stops: List[int]
    load_units: int
    capacity_units: int
    distance_km: float

class RouteMetrics(BaseModel):
    baseline_distance_km: float
    optimized_distance_km: float
    estimated_reduction_pct: float

class RouteOptimizeResponse(BaseModel):
    route_run_id: int
    solver_status: str
    vehicles: List[VehicleRoute]
    metrics: RouteMetrics
