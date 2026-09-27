# API Contract

Base URL: `/api/v1`

## Health

`GET /health`

Response:

```json
{"status":"ok"}
```

## Waste scan

`POST /vision/classify`

Multipart field: `image`

Response:

```json
{
  "success": true,
  "category": "plastic",
  "display_name": "Plastic",
  "source": "yolo",
  "score": 0.94,
  "detections": [
    {
      "category": "plastic",
      "confidence": 0.94,
      "bbox": [12, 34, 200, 310]
    }
  ],
  "disposal": {
    "waste_stream": "Dry recyclable",
    "instructions": ["Empty the item", "Keep it with dry recyclable waste"],
    "special_handling": false,
    "warning": null
  }
}
```

## Pickup requests

`POST /pickups`

```json
{
  "user_id": 2,
  "waste_category": "plastic",
  "latitude": 18.5204,
  "longitude": 73.8567,
  "scheduled_date": "2026-09-27",
  "scheduled_window": "17:00-19:00",
  "load_units": 5,
  "description": "Two bags of recyclable plastic"
}
```

`GET /pickups?status=PENDING`

`GET /pickups/{id}`

`PATCH /pickups/{id}/status`

## Admin analytics

`GET /admin/overview`

Return:

- total requests
- pending
- assigned
- completed
- high priority
- hotspot count
- active vehicles

## Prioritization

`POST /admin/prioritize`

Recalculate priority scores for pending/assigned requests.

## Clustering

`POST /admin/clusters`

Response must include:

- cluster id
- pickup request ids
- centroid
- request count

## Route optimization

`POST /admin/routes/optimize`

Request:

```json
{
  "vehicle_ids": [1,2,3],
  "pickup_request_ids": [1,2,3,4,5,6,7]
}
```

Response:

```json
{
  "route_run_id": 123,
  "solver_status": "SUCCESS",
  "vehicles": [
    {
      "vehicle_id": 1,
      "stops": [3,7,4],
      "load_units": 22,
      "capacity_units": 50,
      "distance_km": 12.4
    }
  ],
  "metrics": {
    "baseline_distance_km": 19.1,
    "optimized_distance_km": 12.4,
    "estimated_reduction_pct": 35.1
  }
}
```

## Error shape

```json
{
  "error": {
    "code": "ROUTE_INFEASIBLE",
    "message": "No feasible route exists for the selected vehicle capacities.",
    "details": {}
  }
}
```
