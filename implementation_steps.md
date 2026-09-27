# Implementation Steps — Strict Order

The coding agent must implement in this order. Do not jump ahead to polish while an earlier acceptance criterion is broken.

## Phase 1 — Skeleton

1. Create `backend/` FastAPI project.
2. Create SQLite database and SQLAlchemy models.
3. Create React/Vite frontend.
4. Add health endpoint.
5. Connect frontend to backend.

Acceptance: frontend loads and shows backend health.

## Phase 2 — Seed data

1. Create waste categories.
2. Create one citizen and one admin.
3. Create 15–25 pickup requests distributed into 3–5 geographic clusters.
4. Create 3 vehicles with capacities.

Acceptance: admin page shows seeded requests.

## Phase 3 — YOLO

1. Add Ultralytics dependency.
2. Load `models/waste_yolo.pt` once at application startup or lazy-load once.
3. Implement image validation and inference service.
4. Normalize checkpoint labels.
5. Return bounding boxes, category, source, score.
6. Add scanner UI.

Acceptance: known demo waste images return visible detections.

## Phase 4 — CLIP fallback

1. Add Transformers/CLIP dependency.
2. Lazy-load CLIP only when needed.
3. Define candidate waste prompts in configuration.
4. Trigger fallback for no detection / low YOLO confidence.
5. Return source=`clip_fallback`.

Acceptance: intentionally ambiguous/low-confidence image reaches CLIP path without crashing.

## Phase 5 — Disposal engine

1. Create local disposal knowledge base.
2. Map category to waste stream and instructions.
3. Attach guidance to vision response.

Acceptance: scanner always produces deterministic guidance for supported categories.

## Phase 6 — Pickup workflow

1. Add pickup creation API.
2. Add request list/detail/status APIs.
3. Build pickup form.
4. Connect citizen scan result to pickup creation.

Acceptance: one scan can lead directly to a pickup request.

## Phase 7 — Priority + DBSCAN

1. Implement transparent priority heuristic.
2. Implement DBSCAN clustering.
3. Add cluster API.
4. Render colored cluster markers.

Acceptance: seeded requests visibly form geographic groups.

## Phase 8 — OR-Tools routing

1. Build Haversine distance matrix.
2. Implement CVRP with vehicle capacities.
3. Add solver time limit.
4. Calculate baseline estimate.
5. Calculate optimized estimate.
6. Save route run and stops.

Acceptance: one button produces route assignments and metrics.

## Phase 9 — Admin polish

1. KPI cards.
2. Priority queue.
3. Map layers.
4. Route results.
5. Request table.
6. Simple statistics.

Acceptance: admin can understand the system without developer explanation.

## Phase 10 — Demo hardening

1. Test all happy paths.
2. Test bad image.
3. Test model missing.
4. Test route infeasible.
5. Test empty requests.
6. Seed a deterministic demo state.
7. Add a reset-demo endpoint or CLI script.

Acceptance: the demo can be restarted from a known state.
