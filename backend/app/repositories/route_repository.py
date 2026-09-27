from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.route import RouteRun, RouteStop
from app.models.vehicle import Vehicle

class RouteRepository:
    @staticmethod
    def get_active_vehicles(db: Session) -> List[Vehicle]:
        return db.query(Vehicle).filter(Vehicle.active == True).all()

    @staticmethod
    def get_vehicles_by_ids(db: Session, ids: List[int]) -> List[Vehicle]:
        return db.query(Vehicle).filter(Vehicle.id.in_(ids), Vehicle.active == True).all()

    @staticmethod
    def create_route_run(
        db: Session,
        solver_status: str,
        optimized_distance: float,
        baseline_distance: float,
        reduction_pct: float,
        vehicle_count: int
    ) -> RouteRun:
        run = RouteRun(
            solver_status=solver_status,
            estimated_total_distance_km=optimized_distance,
            baseline_distance_km=baseline_distance,
            estimated_distance_reduction_pct=reduction_pct,
            vehicle_count=vehicle_count
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def create_route_stops(db: Session, route_run_id: int, vehicle_stops_map: Dict[int, List[int]]):
        for vehicle_id, stop_ids in vehicle_stops_map.items():
            for order, pickup_id in enumerate(stop_ids):
                stop = RouteStop(
                    route_run_id=route_run_id,
                    vehicle_id=vehicle_id,
                    pickup_request_id=pickup_id,
                    stop_order=order + 1,
                    estimated_arrival_minutes=float((order + 1) * 15) # Approx 15 min per stop
                )
                db.add(stop)
        db.commit()

    @staticmethod
    def get_latest_route_run(db: Session) -> Optional[RouteRun]:
        return db.query(RouteRun).order_by(RouteRun.created_at.desc()).first()
