# Testing and Acceptance Criteria

## Backend tests

### Health
- `GET /health` returns 200.

### Vision
- Valid JPEG/PNG accepted.
- Oversized/non-image file rejected.
- YOLO result contains category, score, source, bbox.
- Low-confidence path can invoke CLIP without crashing.
- Unsupported model labels are rejected or explicitly unmapped.

### Disposal
- Every canonical waste class has a deterministic result.
- Missing category returns a controlled error.

### Pickups
- Create request.
- Get request.
- List by status.
- Update status.

### Clustering
- Known nearby points form clusters.
- Isolated point is handled as noise/singleton.
- Missing coordinates are rejected.

### Routing
- Feasible input produces routes.
- Capacity is never exceeded.
- Infeasible capacity produces a structured error.
- Solver respects time limit.
- Every scheduled pickup is accounted for.

## Frontend acceptance

- Upload works.
- Prediction result is shown.
- Disposal card is shown.
- Pickup submission gives success feedback.
- Admin map loads with seeded requests.
- Optimize button visibly transitions to loading state.
- Route results show metrics.
- Errors are displayed without blank screens.

## Demo invariants

For the seeded dataset:

- There are at least 15 pickup requests.
- There are at least 3 vehicles.
- At least 3 geographic clusters are visible.
- Optimization must produce at least one route.
- Before/after distance comparison must be calculated from the same request set.

Do not hard-code the final optimization percentage. Calculate it at runtime.
