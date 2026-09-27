from pydantic import BaseModel
from typing import List

class ClusterItem(BaseModel):
    cluster_id: int
    pickup_request_ids: List[int]
    centroid: List[float]
    request_count: int

class AdminOverview(BaseModel):
    total_requests: int
    pending: int
    assigned: int
    completed: int
    high_priority: int
    hotspot_count: int
    active_vehicles: int
