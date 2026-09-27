# Deployment / Runbook

## Local backend

Windows PowerShell:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If PowerShell execution policy blocks activation, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m app.seed
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Local frontend

```powershell
cd frontend
npm install
npm run dev
```

## Environment variables

Backend `.env.example`:

```text
APP_ENV=development
DATABASE_URL=sqlite:///./smart_waste.db
YOLO_MODEL_PATH=./models/waste_yolo.pt
YOLO_CONFIDENCE_THRESHOLD=0.45
CLIP_ENABLED=true
CLIP_MODEL_NAME=openai/clip-vit-base-patch32
CLIP_TRIGGER_THRESHOLD=0.60
DBSCAN_EPS_METERS=750
DBSCAN_MIN_SAMPLES=2
ROUTE_SOLVER_SECONDS=2
ROAD_FACTOR=1.20
MAX_UPLOAD_MB=8
```

## Hardware

- GPU is optional.
- If CUDA is available, the vision service may use it.
- Otherwise run on CPU.
- Never require CUDA for the application to start.

## Deployment principle

For the hackathon, local execution is the reference environment. Cloud deployment is optional and must not block feature completion.
