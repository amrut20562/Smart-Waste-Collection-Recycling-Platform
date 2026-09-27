import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.waste_category import WasteCategory
from app.models.vehicle import Vehicle
from app.models.pickup import PickupRequest, PickupStatus
from app.services.disposal_service import DISPOSAL_KNOWLEDGE_BASE
from app.services.priority_service import PriorityService

def run_seed(db: Session = None):
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # Recreate tables cleanly
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # 1. Seed Users
        admin_user = User(
            id=1,
            name="Operations Admin",
            email="admin@smartwaste.city",
            role=UserRole.ADMIN
        )
        citizen_user = User(
            id=2,
            name="Priya Sharma",
            email="priya.sharma@example.com",
            role=UserRole.CITIZEN
        )
        db.add_all([admin_user, citizen_user])
        db.commit()

        # 2. Seed Waste Categories
        categories = []
        for code, info in DISPOSAL_KNOWLEDGE_BASE.items():
            cat = WasteCategory(
                code=code,
                display_name=info["display_name"],
                waste_stream=info["waste_stream"],
                instructions="\n".join(info["instructions"]),
                special_handling=info["special_handling"],
                pickup_supported=info["pickup_supported"],
                warning=info["warning"]
            )
            categories.append(cat)
        db.add_all(categories)
        db.commit()

        # 3. Seed Vehicles (Depot Central location: 18.5204, 73.8567 - Pune Central Depot)
        depot_lat, depot_lon = 18.5204, 73.8567
        vehicles = [
            Vehicle(id=1, name="EV Green Hauler 01", capacity_units=40, active=True, start_latitude=depot_lat, start_longitude=depot_lon),
            Vehicle(id=2, name="Eco Truck 02", capacity_units=35, active=True, start_latitude=depot_lat, start_longitude=depot_lon),
            Vehicle(id=3, name="Rapid Collector 03", capacity_units=30, active=True, start_latitude=depot_lat, start_longitude=depot_lon),
        ]
        db.add_all(vehicles)
        db.commit()

        # 4. Seed 20 Realistic Pickup Requests in 4 Distinct Geographic Clusters
        # Base clusters:
        # Cluster A (North-East: Kalyani Nagar / Koregaon Park area ~ 18.536, 73.895)
        # Cluster B (West: Kothrud area ~ 18.507, 73.807)
        # Cluster C (South: Swargate / Mukund Nagar area ~ 18.498, 73.861)
        # Cluster D (North-West: Shivajinagar area ~ 18.530, 73.847)

        sample_pickups = [
            # Cluster A (Kalyani Nagar / Koregaon Park)
            {"user_id": 2, "category": "plastic", "lat": 18.5362, "lon": 73.8951, "date": "2026-09-27", "window": "09:00-11:00", "load": 4, "desc": "Sorted PET plastic bottles and takeout containers"},
            {"user_id": 2, "category": "cardboard", "lat": 18.5380, "lon": 73.8935, "date": "2026-09-27", "window": "09:00-11:00", "load": 6, "desc": "Flattened e-commerce delivery boxes"},
            {"user_id": 2, "category": "compost", "lat": 18.5345, "lon": 73.8970, "date": "2026-09-27", "window": "10:00-12:00", "load": 5, "desc": "Restaurant organic kitchen vegetable waste"},
            {"user_id": 2, "category": "metal", "lat": 18.5372, "lon": 73.8988, "date": "2026-09-27", "window": "11:00-13:00", "load": 3, "desc": "Beverage aluminum cans and clean metal lids"},
            {"user_id": 2, "category": "glass", "lat": 18.5391, "lon": 73.8920, "date": "2026-09-27", "window": "11:00-13:00", "load": 4, "desc": "Glass sauce and beverage bottles (packed safely)"},

            # Cluster B (Kothrud)
            {"user_id": 2, "category": "cardboard", "lat": 18.5071, "lon": 73.8074, "date": "2026-09-27", "window": "14:00-16:00", "load": 8, "desc": "Bulk retail packaging cardboard bundles"},
            {"user_id": 2, "category": "e_waste", "lat": 18.5090, "lon": 73.8055, "date": "2026-09-27", "window": "14:00-16:00", "load": 3, "desc": "Old laptop, cables, and broken electronic tablet"},
            {"user_id": 2, "category": "compost", "lat": 18.5055, "lon": 73.8090, "date": "2026-09-27", "window": "15:00-17:00", "load": 5, "desc": "Residential garden waste and leaves"},
            {"user_id": 2, "category": "plastic", "lat": 18.5085, "lon": 73.8062, "date": "2026-09-27", "window": "15:00-17:00", "load": 3, "desc": "Plastic milk bags and clean grocery wraps"},
            {"user_id": 2, "category": "paper", "lat": 18.5060, "lon": 73.8081, "date": "2026-09-27", "window": "16:00-18:00", "load": 4, "desc": "Old newspapers, office stationery bundles"},

            # Cluster C (Swargate / Mukund Nagar)
            {"user_id": 2, "category": "trash", "lat": 18.4982, "lon": 73.8615, "date": "2026-09-27", "window": "10:00-12:00", "load": 5, "desc": "Commercial non-recyclable dry waste bags"},
            {"user_id": 2, "category": "plastic", "lat": 18.4995, "lon": 73.8630, "date": "2026-09-27", "window": "10:00-12:00", "load": 4, "desc": "Assorted packaging polymers and bottles"},
            {"user_id": 2, "category": "compost", "lat": 18.4970, "lon": 73.8601, "date": "2026-09-27", "window": "11:00-13:00", "load": 6, "desc": "Market surplus fruit and vegetable scraps"},
            {"user_id": 2, "category": "metal", "lat": 18.4965, "lon": 73.8645, "date": "2026-09-27", "window": "13:00-15:00", "load": 3, "desc": "Scrap tin containers and steel fixtures"},
            {"user_id": 2, "category": "glass", "lat": 18.5005, "lon": 73.8590, "date": "2026-09-27", "window": "13:00-15:00", "load": 4, "desc": "Assorted amber and clear glass jars"},

            # Cluster D (Shivajinagar / FC Road)
            {"user_id": 2, "category": "e_waste", "lat": 18.5305, "lon": 73.8475, "date": "2026-09-27", "window": "12:00-14:00", "load": 2, "desc": "Obsolete desktop power supply and mice"},
            {"user_id": 2, "category": "cardboard", "lat": 18.5320, "lon": 73.8450, "date": "2026-09-27", "window": "12:00-14:00", "load": 5, "desc": "Appliance shipping cartons"},
            {"user_id": 2, "category": "plastic", "lat": 18.5290, "lon": 73.8490, "date": "2026-09-27", "window": "14:00-16:00", "load": 4, "desc": "High-density polyethylene containers"},
            {"user_id": 2, "category": "paper", "lat": 18.5335, "lon": 73.8465, "date": "2026-09-27", "window": "14:00-16:00", "load": 3, "desc": "Archived office files and manuals"},
            {"user_id": 2, "category": "compost", "lat": 18.5280, "lon": 73.8480, "date": "2026-09-27", "window": "16:00-18:00", "load": 4, "desc": "Cafeteria food scraps and coffee grounds"},
        ]

        # Insert pickup requests and calculate their initial priority scores
        created_pickups = []
        for p in sample_pickups:
            req = PickupRequest(
                user_id=p["user_id"],
                waste_category=p["category"],
                description=p["desc"],
                latitude=p["lat"],
                longitude=p["lon"],
                scheduled_date=p["date"],
                scheduled_window=p["window"],
                load_units=p["load"],
                priority_score=0.0,
                priority_reasons_json="[]",
                status=PickupStatus.PENDING
            )
            db.add(req)
            created_pickups.append(req)
        db.commit()

        # Update priority scores
        for req in created_pickups:
            score, reasons = PriorityService.calculate_priority(req, created_pickups)
            req.priority_score = score
            req.priority_reasons_json = json.dumps(reasons)
        db.commit()

        print("Database successfully seeded:")
        print(f"- {len(categories)} waste categories")
        print(f"- 2 users (1 admin, 1 citizen)")
        print(f"- {len(vehicles)} vehicles")
        print(f"- {len(created_pickups)} pickup requests across 4 geographic clusters")

    finally:
        if should_close:
            db.close()

if __name__ == "__main__":
    run_seed()
