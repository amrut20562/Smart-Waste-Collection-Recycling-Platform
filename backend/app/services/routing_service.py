import math
import logging
from typing import List, Dict, Any, Tuple
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from app.config import settings
from app.models.pickup import PickupRequest
from app.models.vehicle import Vehicle

logger = logging.getLogger(__name__)

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

class RoutingService:
    @classmethod
    def calculate_distance_matrix(cls, locations: List[Tuple[float, float]], road_factor: float = None) -> List[List[int]]:
        if road_factor is None:
            road_factor = settings.ROAD_FACTOR
        num_locs = len(locations)
        matrix = [[0] * num_locs for _ in range(num_locs)]
        for i in range(num_locs):
            for j in range(num_locs):
                if i != j:
                    dist_km = haversine_distance_km(
                        locations[i][0], locations[i][1],
                        locations[j][0], locations[j][1]
                    )
                    # Convert to meters as integer for OR-Tools solver
                    matrix[i][j] = int(dist_km * road_factor * 1000)
        return matrix

    @classmethod
    def compute_baseline_distance(cls, depot_loc: Tuple[float, float], pickup_locs: List[Tuple[float, float]], road_factor: float = None) -> float:
        """
        Baseline distance: depot -> visit each pending request in submission/order -> return to depot.
        """
        if not pickup_locs:
            return 0.0
        if road_factor is None:
            road_factor = settings.ROAD_FACTOR

        total_km = 0.0
        curr_loc = depot_loc
        for loc in pickup_locs:
            total_km += haversine_distance_km(curr_loc[0], curr_loc[1], loc[0], loc[1]) * road_factor
            curr_loc = loc
        # Return to depot
        total_km += haversine_distance_km(curr_loc[0], curr_loc[1], depot_loc[0], depot_loc[1]) * road_factor
        return round(total_km, 2)

    @classmethod
    def optimize_routes(cls, vehicles: List[Vehicle], pickups: List[PickupRequest]) -> Dict[str, Any]:
        if not pickups:
            raise ValueError("No pickup requests provided for optimization")
        if not vehicles:
            raise ValueError("No active vehicles available for optimization")

        # Total capacity check
        total_capacity = sum(v.capacity_units for v in vehicles)
        total_demand = sum(p.load_units for p in pickups)
        if total_demand > total_capacity:
            raise ValueError(
                f"ROUTE_INFEASIBLE: Total pickup load ({total_demand} units) exceeds total fleet capacity ({total_capacity} units)."
            )

        # Common central depot from first vehicle
        depot_lat = vehicles[0].start_latitude
        depot_lon = vehicles[0].start_longitude
        depot_loc = (depot_lat, depot_lon)

        locations = [depot_loc] + [(p.latitude, p.longitude) for p in pickups]
        pickup_locs = [(p.latitude, p.longitude) for p in pickups]
        demands = [0] + [p.load_units for p in pickups]
        vehicle_capacities = [v.capacity_units for v in vehicles]
        num_vehicles = len(vehicles)
        depot_index = 0

        distance_matrix = cls.calculate_distance_matrix(locations)

        # Baseline distance calculation
        baseline_km = cls.compute_baseline_distance(depot_loc, pickup_locs)

        # Create Routing Index Manager
        manager = pywrapcp.RoutingIndexManager(len(locations), num_vehicles, depot_index)
        routing = pywrapcp.RoutingModel(manager)

        # Distance callback
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Demand callback & capacity constraint
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return demands[from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            vehicle_capacities,  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity"
        )

        # Setting search parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = settings.ROUTE_SOLVER_SECONDS

        # Solve the problem
        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            raise ValueError("ROUTE_INFEASIBLE: Solver could not find a feasible routing solution within constraints.")

        # Extract solution
        vehicle_routes: List[Dict[str, Any]] = []
        total_optimized_distance_m = 0

        for v_idx, vehicle in enumerate(vehicles):
            index = routing.Start(v_idx)
            stops: List[int] = []
            route_load = 0
            route_distance_m = 0

            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                if node_index != depot_index:
                    pickup_req = pickups[node_index - 1]
                    stops.append(pickup_req.id)
                    route_load += pickup_req.load_units

                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance_m += routing.GetArcCostForVehicle(previous_index, index, v_idx)

            v_dist_km = round(route_distance_m / 1000.0, 2)
            total_optimized_distance_m += route_distance_m

            vehicle_routes.append({
                "vehicle_id": vehicle.id,
                "stops": stops,
                "load_units": route_load,
                "capacity_units": vehicle.capacity_units,
                "distance_km": v_dist_km
            })

        optimized_km = round(total_optimized_distance_m / 1000.0, 2)

        # Calculate reduction percentage
        if baseline_km > 0:
            reduction_pct = round(max(0.0, ((baseline_km - optimized_km) / baseline_km) * 100.0), 1)
        else:
            reduction_pct = 0.0

        return {
            "solver_status": "SUCCESS",
            "vehicles": vehicle_routes,
            "metrics": {
                "baseline_distance_km": baseline_km,
                "optimized_distance_km": optimized_km,
                "estimated_reduction_pct": reduction_pct
            }
        }
