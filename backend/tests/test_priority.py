from datetime import datetime, timezone, timedelta
from app.models.pickup import PickupRequest
from app.services.priority_service import PriorityService

def test_priority_calculation():
    p1 = PickupRequest(
        id=1,
        user_id=2,
        waste_category="compost",
        latitude=18.5204,
        longitude=73.8567,
        scheduled_date="2026-09-27",
        load_units=6,
        created_at=datetime.now(timezone.utc) - timedelta(hours=15)
    )

    p2 = PickupRequest(
        id=2,
        user_id=2,
        waste_category="paper",
        latitude=18.5210,
        longitude=73.8570,
        scheduled_date="2026-09-28",
        load_units=1,
        created_at=datetime.now(timezone.utc)
    )

    score1, reasons1 = PriorityService.calculate_priority(p1, [p1, p2])
    score2, reasons2 = PriorityService.calculate_priority(p2, [p1, p2])

    # Organic waste with long waiting time and higher load should score higher priority
    assert score1 > score2
    assert len(reasons1) > 0
    assert 0.0 <= score1 <= 100.0
