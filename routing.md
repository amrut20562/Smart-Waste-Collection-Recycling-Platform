# Clustering and Route Optimization

## Priority score

Use a transparent deterministic score from 0–100.

Suggested weighted components:

```text
waiting_time       30%
waste_urgency       25%
scheduled_overdue  20%
cluster_density    15%
historical_issue    10%
```

The implementation may simplify this, but the score must be explainable.

Example reasons:

- `Waiting 8.2 hours`
- `Organic waste is treated as higher urgency`
- `Pickup window is overdue`
- `6 other requests are nearby`

Do not label a score as scientifically validated. It is an operational heuristic for the demo.

## DBSCAN

1. Collect latitude/longitude from pending requests.
2. Convert coordinates into a meter-based representation before DBSCAN, or use a geospatial-safe distance approach.
3. Default `eps`: 750 meters for demo data.
4. Default `min_samples`: 2.
5. Noise points remain individual requests.
6. Return cluster membership to the UI.

The values must be config-driven.

## Baseline distance

For demo comparison, define a transparent baseline:

`baseline = depot -> each pending request in creation order -> depot`

This is a baseline estimate, not a claim about an actual municipal collection route.

## Distance matrix

Use Haversine distance in kilometers for the no-paid-API MVP.

Optionally multiply straight-line distance by a configurable road-factor (default `1.20`) to make the estimate less optimistic. Label the resulting metric `estimated distance`.

## OR-Tools

Model the route problem as a Capacitated Vehicle Routing Problem (CVRP).

Inputs:

- depot/start location per vehicle
- pickup locations
- distance matrix
- pickup load units
- vehicle capacities

Objective:

- minimize total estimated travel distance

Constraints:

- each selected pickup is visited at most once and, by default, exactly once when feasible
- vehicle load must not exceed capacity
- inactive vehicles cannot receive stops
- solver time limit: 2 seconds

Use `PATH_CHEAPEST_ARC` for the initial solution and `GUIDED_LOCAL_SEARCH` when available/appropriate.

OR-Tools officially supports vehicle routing, capacity constraints, time windows, and solver search/time limits; see `sources.md`.

## Route UI

For each route show:

- vehicle
- stop order
- number of pickups
- load/capacity
- estimated distance
- estimated duration if available

Also show the before/after comparison.
