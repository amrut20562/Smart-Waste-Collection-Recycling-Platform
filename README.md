# Smart Waste AI — Smart Waste Collection & Recycling Platform

A software-only waste collection and recycling platform with two surfaces: a **Citizen App** (waste identification and pickup requests) and an **Admin Command Center** (request management, geographic clustering, and route optimization using OR-Tools CVRP).

## Quick Start

### 1. Backend Setup (Python 3.11+)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed     # Seeds database with demo data
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

### 2. Frontend Setup (Node.js 20+)

```powershell
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 3. Demo Flow

1. Open the frontend in your browser.
2. Click **Citizen Portal** to scan waste images and request pickup.
3. Click **Operations Center** to view the admin dashboard, find geographic clusters, and run route optimization.
4. The demo comes pre-seeded with 20+ pickup requests across 4 geographic clusters and 3 vehicles.

## Architecture

```
┌─────────────────────┐     REST/JSON      ┌─────────────────────┐
│   React Frontend    │ ◄────────────────► │    FastAPI Backend  │
│   (Citizen + Admin) │                    │                     │
└─────────────────────┘                    └──────────┬──────────┘
                                                       │
                                            ┌──────────┴──────────┐
                                            │                     │
                                      Vision Service         Operations Service
                                            │                     │
                                      YOLO + CLIP          DBSCAN + OR-Tools
                                            │                     │
                                      Disposal Engine       Routing Engine
                                            │                     │
                                            └──────────┬──────────┘
                                                       │
                                                SQLite Database
```

## AI Pipeline

```
Image
  → YOLO11n waste detector (primary)
  → CLIP zero-shot semantic fallback (when YOLO confidence < 0.60)
  → Canonical waste category
  → Disposal knowledge base
  → Pickup request
```

## Optimization Pipeline

```
Pending pickup requests
  → Priority scoring (transparent heuristic)
  → DBSCAN geographic clustering (eps=750m, min_samples=2)
  → Haversine distance matrix × road_factor (1.20)
  → OR-Tools CVRP (capacity-constrained vehicle routing)
  → Optimized routes with baseline comparison
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/vision/classify` | Waste image classification |
| POST | `/api/v1/pickups` | Create pickup request |
| GET | `/api/v1/pickups` | List pickups (optional `?status=PENDING`) |
| GET | `/api/v1/admin/overview` | Admin dashboard KPIs |
| POST | `/api/v1/admin/clusters` | Run DBSCAN clustering |
| POST | `/api/v1/admin/routes/optimize` | Run OR-Tools route optimization |
| POST | `/api/v1/admin/reset-demo` | Reset database to seed state |

## Tech Stack

- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, React Router, Leaflet, Recharts, Lucide React
- **Backend**: FastAPI, SQLAlchemy 2.x, Pydantic v2, SQLite
- **Computer Vision**: Ultralytics YOLO, Hugging Face Transformers CLIP
- **ML/Optimization**: scikit-learn (DBSCAN), Google OR-Tools (CVRP)
- **Mapping**: Leaflet + OpenStreetMap tiles

## Environment Variables (Backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./smart_waste.db` | SQLite database path |
| `YOLO_MODEL_PATH` | `./models/waste_yolo.pt` | Path to YOLO weights |
| `YOLO_CONFIDENCE_THRESHOLD` | `0.45` | YOLO detection threshold |
| `CLIP_ENABLED` | `true` | Enable CLIP fallback |
| `CLIP_TRIGGER_THRESHOLD` | `0.60` | YOLO confidence threshold to trigger CLIP |
| `DBSCAN_EPS_METERS` | `750` | DBSCAN epsilon in meters |
| `ROUTE_SOLVER_SECONDS` | `2` | OR-Tools time limit |
| `ROAD_FACTOR` | `1.20` | Straight-line to road distance multiplier |

## Running Tests

```powershell
# Backend tests
cd backend
.\.venv\Scripts\activate
pytest tests/

# Frontend build
cd frontend
npm run build
```

## Demo Script (2 Minutes)

1. **Citizen AI (0:15)**: Upload a waste image, see YOLO detection, CLIP fallback, disposal guidance.
2. **Pickup Request (0:35)**: Submit a pickup request from the scan result.
3. **Admin Dashboard (0:45)**: View 20+ seeded requests on the interactive map.
4. **Cluster View (1:00)**: Click "Find Clusters" to group nearby requests.
5. **Optimize Routes (1:15)**: Click "Optimize Collection" to generate capacity-constrained vehicle routes.
6. **Route Comparison (1:40)**: Compare baseline vs. optimized distance, see percentage savings.

## License

MIT License