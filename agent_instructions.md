# Coding Agent Master Instructions

You are implementing the Smart Waste AI hackathon MVP described by the repository specification.

## Non-negotiable behavior

1. Read all files in `docs/` before coding.
2. Treat `hard_constraints.md` as higher priority than optional feature requests.
3. Never silently substitute a different architecture.
4. Never add paid APIs.
5. Never add model training.
6. Never replace OR-Tools routing with an LLM.
7. Never use an LLM to invent disposal rules.
8. Prefer a working simple implementation over a sophisticated incomplete one.
9. Keep frontend/backend interfaces aligned with `api_contract.md`.
10. Add/update tests for every completed service.

## Implementation style

- TypeScript strict mode.
- Python type hints for service/API code.
- Small single-purpose service classes/functions.
- No hidden global mutable state except the loaded model cache.
- Load YOLO once; do not load the model on every request.
- Lazy-load CLIP to reduce startup cost.
- Keep model and optimization configuration in environment variables.
- Use structured logging.
- Return predictable error JSON.

## AI behavior

- YOLO is primary.
- CLIP is fallback.
- Keep the source of classification visible in the API response.
- Preserve bounding boxes for YOLO results.
- Never fabricate confidence values.

## Routing behavior

- DBSCAN clusters first.
- OR-Tools solves routes second.
- Haversine distance is acceptable for the no-paid-API MVP and must be labelled estimated.
- Capacity constraints are mandatory.
- Route solver time limit is mandatory.

## Data behavior

- Seed deterministic data so a judge can reproduce the same demo.
- Do not depend on external databases or external geocoding for the core flow.

## Completion gate

Before declaring the project complete, run:

1. backend tests
2. frontend build
3. health check
4. image classification test
5. pickup creation test
6. clustering test
7. route optimization test
8. end-to-end demo test

If any core step fails, fix it before implementing optional features.
