# Architecture

## High-level architecture

```text
┌───────────────────────────────────────────────────────────┐
│                       React Frontend                       │
│                                                           │
│ Citizen App                     Admin Command Center       │
│ - Waste Scan                    - Requests                 │
│ - Disposal Guide                - Map                      │
│ - Pickup Request                - Priority                 │
│ - Tracking                      - Clusters                 │
│                                 - Route Optimization        │
└───────────────────────────┬───────────────────────────────┘
                            │ REST/JSON
                            ▼
┌───────────────────────────────────────────────────────────┐
│                    FastAPI Backend                         │
│                                                           │
│ API routers → Services → Repositories                      │
│                │                                          │
│        ┌───────┼───────────────────────────────┐          │
│        │       │                               │          │
│      Vision  Disposal                      Operations      │
│        │       │                               │          │
│   YOLO + CLIP │                         DBSCAN + OR-Tools   │
│        │       │                               │          │
│        └───────┴───────────────┬───────────────┘          │
│                                │                          │
│                              SQLite                       │
└───────────────────────────────────────────────────────────┘
```

## Layering

### API layer
Only handles request validation, response serialization, HTTP status codes, and dependency injection.

### Service layer
Contains business logic:

- `VisionService`
- `DisposalService`
- `PickupService`
- `PriorityService`
- `ClusteringService`
- `RoutingService`
- `AnalyticsService`

### Repository layer
Contains database access. Do not put optimization or model logic inside SQL code.

### Model layer
Contains SQLAlchemy models and Pydantic schemas.

## AI pipeline

```text
Uploaded image
    │
    ▼
Image validation
    │
    ▼
YOLO inference
    │
    ├── confident detection ──────────────┐
    │                                     │
    └── uncertain/no detection            │
                 │                         │
                 ▼                         │
              CLIP                        │
                 │                         │
                 └──────────────┬──────────┘
                                ▼
                     Canonical waste class
                                ▼
                     Disposal knowledge base
                                ▼
                     Pickup request (optional)
```

## Operations pipeline

```text
Pending pickup requests
        │
        ▼
Validate coordinates + load units
        │
        ▼
Priority score
        │
        ▼
DBSCAN clusters
        │
        ▼
Distance matrix
        │
        ▼
OR-Tools CVRP
        │
        ▼
Route assignments
        │
        ▼
Dashboard metrics + map
```

## State flow

Pickup request status:

`PENDING -> ASSIGNED -> IN_PROGRESS -> COMPLETED`

Alternative terminal state:

`PENDING/ASSIGNED -> CANCELLED`

Do not create additional statuses unless required by the UI.
