from sqlalchemy.orm import Session
from app.models.pickup import PickupRequest, PickupStatus
from app.models.vehicle import Vehicle
from app.services.clustering_service import ClusteringService

class AnalyticsService:
    @staticmethod
    def get_admin_overview(db: Session):
        total_requests = db.query(PickupRequest).count()
        pending = db.query(PickupRequest).filter(PickupRequest.status == PickupStatus.PENDING).count()
        assigned = db.query(PickupRequest).filter(PickupRequest.status == PickupStatus.ASSIGNED).count()
        completed = db.query(PickupRequest).filter(PickupRequest.status == PickupStatus.COMPLETED).count()
        high_priority = db.query(PickupRequest).filter(
            PickupRequest.status == PickupStatus.PENDING,
            PickupRequest.priority_score >= 70.0
        ).count()

        pending_pickups = db.query(PickupRequest).filter(PickupRequest.status == PickupStatus.PENDING).all()
        clusters = ClusteringService.cluster_pickups(pending_pickups)
        hotspot_count = len([c for c in clusters if c["request_count"] >= 3])

        active_vehicles = db.query(Vehicle).filter(Vehicle.active == True).count()

        return {
            "total_requests": total_requests,
            "pending": pending,
            "assigned": assigned,
            "completed": completed,
            "high_priority": high_priority,
            "hotspot_count": hotspot_count,
            "active_vehicles": active_vehicles
        }
