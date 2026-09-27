import pytest
from app.models.pickup import PickupRequest
from app.models.vehicle import Vehicle
from app.services.routing_service import RoutingService, haversine_distance_km

def test_haversine_distance():
    # Distance between Pune Railway Station and Shaniwar Wada is ~2.5km
    dist = haversine_distance_km(18.5284, 73.8743, 18.5196, 73.8553)
    assert 2.0 < dist < 3.5

def test_routing_optimization_feasible():
    vehicles = [
        Vehicle(id=1, name="Hauler 1", capacity_units=20, active=True, start_latitude=18.5204, start_longitude=73.8567),
        Vehicle(id=2, name="Hauler 2", capacity_units=20, active=True, start_latitude=18.5204, start_longitude=73.8567),
    ]

    pickups = [
        PickupRequest(id=1, latitude=18.5362, longitude=73.8951, load_units=4),
        PickupRequest(id=2, latitude=18.5380, longitude=73.8935, load_units=5),
        PickupRequest(id=3, latitude=18.5071, longitude=73.8074, load_units=6),
        PickupRequest(id=4, latitude=18.5090, longitude=73.8055, load_units=3),
    ]

    result = RoutingService.optimize_routes(vehicles, pickups)
    assert result["solver_status"] == "SUCCESS"
    assert "metrics" in result
    assert result["metrics"]["baseline_distance_km"] > 0
    assert result["metrics"]["optimized_distance_km"] > 0
    assert result["metrics"]["estimated_reduction_pct"] >= 0

    assigned_stops = []
    for v in result["vehicles"]:
        assert v["load_units"] <= v["capacity_units"]
        assigned_stops.extend(v["stops"])

    assert set(assigned_stops) == {1, 2, 3, 4}

def test_routing_infeasible_capacity():
    vehicles = [
        Vehicle(id=1, name="Small Hauler", capacity_units=5, active=True, start_latitude=18.5204, start_longitude=73.8567)
    ]
    pickups = [
        PickupRequest(id=1, latitude=18.5362, longitude=73.8951, load_units=10)
    ]

    with pytest.raises(ValueError) as exc:
        RoutingService.optimize_routes(vehicles, pickups)
    assert "ROUTE_INFEASIBLE" in str(exc.value)
