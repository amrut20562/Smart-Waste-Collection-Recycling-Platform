import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.schemas.pickup import PickupCreate, PickupResponse, PickupStatusUpdate
from app.models.pickup import PickupStatus, PickupRequest
from app.repositories.pickup_repository import PickupRepository
from app.services.priority_service import PriorityService

router = APIRouter()

@router.post("/pickups", response_model=PickupResponse)
def create_pickup(data: PickupCreate, db: Session = Depends(get_db)):
    # Calculate initial priority
    all_pending = PickupRepository.get_all(db, status=PickupStatus.PENDING)

    # Temporary instance for score calculation
    temp_obj = PickupRequest(
        user_id=data.user_id,
        waste_category=data.waste_category,
        latitude=data.latitude,
        longitude=data.longitude,
        scheduled_date=data.scheduled_date,
        load_units=data.load_units
    )
    score, reasons = PriorityService.calculate_priority(temp_obj, all_pending)

    pickup = PickupRepository.create(
        db,
        data,
        priority_score=score,
        priority_reasons=json.dumps(reasons)
    )
    return pickup

@router.get("/pickups", response_model=List[PickupResponse])
def get_pickups(
    status: Optional[PickupStatus] = Query(None),
    db: Session = Depends(get_db)
):
    return PickupRepository.get_all(db, status=status)

@router.get("/pickups/{pickup_id}", response_model=PickupResponse)
def get_pickup(pickup_id: int, db: Session = Depends(get_db)):
    pickup = PickupRepository.get_by_id(db, pickup_id)
    if not pickup:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": f"Pickup request #{pickup_id} not found."}}
        )
    return pickup

@router.patch("/pickups/{pickup_id}/status", response_model=PickupResponse)
def update_pickup_status(
    pickup_id: int,
    data: PickupStatusUpdate,
    db: Session = Depends(get_db)
):
    pickup = PickupRepository.update_status(db, pickup_id, data.status)
    if not pickup:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": f"Pickup request #{pickup_id} not found."}}
        )
    return pickup
