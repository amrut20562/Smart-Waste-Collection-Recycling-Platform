import json
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any
from app.models.pickup import PickupRequest

# Urgency mapping by waste category
WASTE_URGENCY_MAP = {
    "compost": 95,   # Organic rots fast, causes odor/pests
    "e_waste": 80,   # Hazardous / high value
    "glass": 70,     # Safety / breakage risk
    "trash": 65,     # General bin overflow
    "metal": 50,     # Recyclable
    "plastic": 45,   # Recyclable dry
    "cardboard": 40, # Recyclable bulky
    "paper": 35      # Dry recyclable
}

class PriorityService:
    @classmethod
    def calculate_priority(cls, pickup: PickupRequest, all_pending: List[PickupRequest]) -> Tuple[float, List[str]]:
        reasons: List[str] = []
        now = datetime.now(timezone.utc)

        # 1. Waiting time component (30%)
        # Calculate hours since creation
        if pickup.created_at:
            created_at = pickup.created_at.replace(tzinfo=timezone.utc) if pickup.created_at.tzinfo is None else pickup.created_at
            hours_waiting = max(0.0, (now - created_at).total_seconds() / 3600.0)
        else:
            hours_waiting = 2.0

        # Scale 0 to 48 hours -> 0 to 100
        waiting_score = min(100.0, (hours_waiting / 24.0) * 100.0)
        if hours_waiting >= 12.0:
            reasons.append(f"Waiting for {hours_waiting:.1f} hours")
        elif hours_waiting >= 4.0:
            reasons.append(f"In queue for {hours_waiting:.1f} hours")

        # 2. Waste urgency component (25%)
        urgency_score = WASTE_URGENCY_MAP.get(pickup.waste_category.lower(), 50)
        if pickup.waste_category.lower() == "compost":
            reasons.append("Organic waste has high decomposition urgency")
        elif pickup.waste_category.lower() == "e_waste":
            reasons.append("E-waste requires priority hazardous handling")
        elif pickup.waste_category.lower() == "glass":
            reasons.append("Glass items carry fragile handling priority")

        # 3. Scheduled / Overdue component (20%)
        overdue_score = 30.0 # Default scheduled baseline
        try:
            scheduled_dt = datetime.strptime(pickup.scheduled_date, "%Y-%m-%d").date()
            today_dt = now.date()
            if scheduled_dt < today_dt:
                overdue_score = 100.0
                reasons.append("Pickup date is overdue")
            elif scheduled_dt == today_dt:
                overdue_score = 75.0
                reasons.append("Scheduled for collection today")
        except Exception:
            pass

        # 4. Cluster density component (15%)
        # Count other pending requests within ~1km
        nearby_count = 0
        for other in all_pending:
            if other.id != pickup.id and other.latitude and other.longitude:
                # Approx lat/lon delta for 1km is ~0.009 deg
                lat_diff = abs(other.latitude - pickup.latitude)
                lon_diff = abs(other.longitude - pickup.longitude)
                if (lat_diff**2 + lon_diff**2)**0.5 < 0.015:
                    nearby_count += 1

        density_score = min(100.0, (nearby_count / 5.0) * 100.0)
        if nearby_count >= 2:
            reasons.append(f"{nearby_count} other requests located in immediate vicinity")

        # 5. Load size / bulk component (10%)
        load_score = min(100.0, (pickup.load_units / 10.0) * 100.0)
        if pickup.load_units >= 5:
            reasons.append(f"Large volume batch ({pickup.load_units} load units)")

        # Weighted calculation
        total_score = (
            waiting_score * 0.30 +
            urgency_score * 0.25 +
            overdue_score * 0.20 +
            density_score * 0.15 +
            load_score * 0.10
        )

        final_score = round(max(0.0, min(100.0, total_score)), 1)
        if not reasons:
            reasons.append("Standard priority queue placement")

        return final_score, reasons
