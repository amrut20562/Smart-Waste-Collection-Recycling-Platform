from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.pickup import PickupRequest, PickupStatus
from app.schemas.pickup import PickupCreate

class PickupRepository:
    @staticmethod
    def get_all(db: Session, status: Optional[PickupStatus] = None) -> List[PickupRequest]:
        query = db.query(PickupRequest)
        if status:
            query = query.filter(PickupRequest.status == status)
        return query.order_by(PickupRequest.priority_score.desc(), PickupRequest.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, pickup_id: int) -> Optional[PickupRequest]:
        return db.query(PickupRequest).filter(PickupRequest.id == pickup_id).first()

    @staticmethod
    def create(db: Session, data: PickupCreate, priority_score: float = 0.0, priority_reasons: str = "[]") -> PickupRequest:
        obj = PickupRequest(
            user_id=data.user_id,
            waste_category=data.waste_category,
            description=data.description,
            latitude=data.latitude,
            longitude=data.longitude,
            scheduled_date=data.scheduled_date,
            scheduled_window=data.scheduled_window,
            load_units=data.load_units,
            priority_score=priority_score,
            priority_reasons_json=priority_reasons,
            status=PickupStatus.PENDING
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def update_status(db: Session, pickup_id: int, status: PickupStatus) -> Optional[PickupRequest]:
        obj = db.query(PickupRequest).filter(PickupRequest.id == pickup_id).first()
        if obj:
            obj.status = status
            db.commit()
            db.refresh(obj)
        return obj

    @staticmethod
    def update_priority(db: Session, pickup_id: int, score: float, reasons_json: str):
        obj = db.query(PickupRequest).filter(PickupRequest.id == pickup_id).first()
        if obj:
            obj.priority_score = score
            obj.priority_reasons_json = reasons_json
            db.commit()
