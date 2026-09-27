import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.schemas.analytics import AdminOverview, ClusterItem
from app.schemas.route import RouteOptimizeRequest, RouteOptimizeResponse
from app.models.pickup import PickupStatus, PickupRequest
from app.models.vehicle import Vehicle
from app.repositories.pickup_repository import PickupRepository
from app.repositories.route_repository import RouteRepository
from app.services.analytics_service import AnalyticsService
from app.services.priority_service import PriorityService
from app.services.clustering_service import ClusteringService
from app.services.routing_service import RoutingService

router = APIRouter()

@router.get("/admin/overview", response_model=AdminOverview)
def get_admin_overview(db: Session = Depends(get_db)):
    return AnalyticsService.get_admin_overview(db)

@router.get("/admin/vehicles")
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return vehicles

@router.post("/admin/prioritize")
def recalculate_priorities(db: Session = Depends(get_db)):
    pending_pickups = PickupRepository.get_all(db, status=PickupStatus.PENDING)
    updated_count = 0
    for pickup in pending_pickups:
        score, reasons = PriorityService.calculate_priority(pickup, pending_pickups)
        PickupRepository.update_priority(db, pickup.id, score, json.dumps(reasons))
        updated_count += 1
    return {"status": "success", "updated_count": updated_count}

@router.post("/admin/clusters", response_model=List[ClusterItem])
def get_clusters(db: Session = Depends(get_db)):
    pending_pickups = PickupRepository.get_all(db, status=PickupStatus.PENDING)
    clusters = ClusteringService.cluster_pickups(pending_pickups)
    return clusters

@router.post("/admin/routes/optimize", response_model=RouteOptimizeResponse)
def optimize_routes(data: RouteOptimizeRequest, db: Session = Depends(get_db)):
    vehicles = RouteRepository.get_vehicles_by_ids(db, data.vehicle_ids)
    if not vehicles:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "NO_VEHICLES", "message": "No valid active vehicles selected for route optimization."}}
        )

    pickups: List[PickupRequest] = []
    for pid in data.pickup_request_ids:
        p = PickupRepository.get_by_id(db, pid)
        if p and p.status == PickupStatus.PENDING:
            pickups.append(p)

    if not pickups:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "NO_PICKUPS", "message": "No valid pending pickup requests selected for optimization."}}
        )

    try:
        result = RoutingService.optimize_routes(vehicles, pickups)

        # Save route run and stops to database
        route_run = RouteRepository.create_route_run(
            db=db,
            solver_status=result["solver_status"],
            optimized_distance=result["metrics"]["optimized_distance_km"],
            baseline_distance=result["metrics"]["baseline_distance_km"],
            reduction_pct=result["metrics"]["estimated_reduction_pct"],
            vehicle_count=len(result["vehicles"])
        )

        vehicle_stops_map = {
            v["vehicle_id"]: v["stops"]
            for v in result["vehicles"]
            if v["stops"]
        }
        RouteRepository.create_route_stops(db, route_run.id, vehicle_stops_map)

        # Mark scheduled pickups as ASSIGNED
        for v in result["vehicles"]:
            for pid in v["stops"]:
                PickupRepository.update_status(db, pid, PickupStatus.ASSIGNED)

        return {
            "route_run_id": route_run.id,
            "solver_status": result["solver_status"],
            "vehicles": result["vehicles"],
            "metrics": result["metrics"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "ROUTE_INFEASIBLE", "message": str(e)}}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": {"code": "OPTIMIZATION_FAILED", "message": f"Route optimization solver failed: {str(e)}"}}
        )

@router.post("/admin/reset-demo")
def reset_demo_data(db: Session = Depends(get_db)):
    from app.seed import run_seed
    run_seed(db)
    return {"status": "success", "message": "Demo database successfully reset and seeded."}
