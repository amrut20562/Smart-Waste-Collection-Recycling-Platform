# Hard Constraints

These rules are mandatory for the coding agent. Do not violate them to add extra features.

## Time and scope

- Optimize for a 4-hour solo hackathon MVP.
- Core functionality must work before optional polish.
- Do not implement features outside this specification unless explicitly requested by the user.
- Do not start model training or dataset annotation during the hackathon build.
- Do not add a feature merely because it is technically interesting.

## Cost

- No paid APIs.
- No paid map providers.
- No paid LLM APIs.
- No cloud database requirement.
- The application must run locally with seeded data.

## Architecture

- One frontend application.
- One FastAPI backend.
- One local SQLite database.
- No microservices.
- No Kubernetes.
- No message queue.
- No Redis unless a later requirement makes it necessary.
- ML inference runs inside the FastAPI backend for the MVP.

## AI

- YOLO is the primary visual model.
- Use a waste-specific YOLO checkpoint supplied as `models/waste_yolo.pt`.
- Do not train a detector in the application runtime.
- CLIP is the semantic fallback, not the primary detector.
- CLIP must only run when YOLO is uncertain or returns no usable waste detection.
- Never invent disposal rules from an LLM.
- Disposal guidance must come from a deterministic local knowledge base.

## Optimization

- DBSCAN is responsible for geographic pickup clustering.
- OR-Tools is responsible for vehicle-route optimization.
- Do not replace OR-Tools with an LLM.
- Route distances are explicitly labelled `estimated` when derived from Haversine/geometric distance instead of a live road-routing provider.
- Solver execution must have a hard time limit; default to 2 seconds for the MVP.

## Data

- SQLite only.
- Seed demo data must be included.
- IDs are UUID strings or stable integer IDs; use one convention consistently.
- Store latitude/longitude directly on pickup requests for deterministic demos.
- Do not require geocoding to submit a request.

## Security

- No real patient/medical/financial data.
- Do not store unnecessary personal data.
- Uploaded images are stored locally and may be deleted after inference if not needed.
- Demo authentication may use seeded local users/role selection; do not spend hackathon time on OAuth/SSO.

## UI

- Responsive desktop-first dashboard.
- Mobile citizen flow must remain usable.
- Every AI decision shown to the user must include human-readable evidence or explanation.
- Avoid fake metrics that are presented as real-world measurements. Demo estimates must be labelled.

## Reliability

- If YOLO is unavailable, the app must show a clear `AI unavailable` message rather than silently producing a fabricated classification.
- If CLIP is unavailable, continue with YOLO if it has a confident result.
- If OR-Tools cannot find a route, return a structured error and show the unscheduled requests.
- API errors must be JSON and user-readable.

## Environment

- Python 3.11.
- Node.js 20 LTS.
- Windows 11 local development must be supported.
- CUDA acceleration is optional; CPU inference must still function.
