# Tech Stack

## Frontend

- React 18/19-compatible codebase using Vite.
- TypeScript.
- Tailwind CSS.
- React Router.
- Axios or native `fetch`; choose one and use it consistently. Prefer native `fetch` to minimize dependencies.
- Leaflet + React-Leaflet for the operations map.
- Lucide React for icons.
- Recharts for lightweight dashboard charts.

## Backend

- Python 3.11.
- FastAPI.
- Uvicorn.
- Pydantic v2.
- SQLAlchemy 2.x.
- SQLite.
- Python `multipart`/FastAPI UploadFile for image uploads.

## Computer vision

### Primary: YOLO

- Ultralytics YOLO.
- Recommended runtime model family: YOLO11n or a compatible lightweight waste-specific YOLO checkpoint.
- Model path: `models/waste_yolo.pt`.
- The checkpoint must be a detection model whose class names are mapped into the application's canonical waste taxonomy.
- Input images are resized/letterboxed by the inference library.
- Default detection confidence threshold: `0.45`.
- Default NMS IoU threshold: `0.50` unless the selected checkpoint requires otherwise.

### Fallback: CLIP

- Hugging Face Transformers.
- Default: `openai/clip-vit-base-patch32`.
- Use zero-shot image classification with explicitly written candidate prompts.
- Default CLIP activation condition: YOLO returns no usable detection OR the top useful YOLO confidence is below `0.60`.
- Do not claim CLIP confidence is calibrated probability.

CLIP supports zero-shot image classification by comparing image and text embeddings; the Transformers documentation exposes this through the zero-shot-image-classification pipeline. See `sources.md`.

## ML utilities

- PyTorch.
- torchvision.
- Pillow.
- NumPy.
- scikit-learn for DBSCAN.

## Optimization

- Google OR-Tools Python package for vehicle routing.
- Use a distance matrix generated from Haversine/geometric distance for the no-paid-API MVP.
- Use vehicle capacity as a first-class route constraint.
- Optional pickup time windows may be supported only after the core route works.

## Mapping

- Leaflet.
- OpenStreetMap tiles for the demo where internet access exists.
- Never hard-depend on a paid geocoding or directions API.
- The application must still show coordinates/routes if tile loading fails.

## Tooling

- Git.
- Python virtual environment (`.venv`).
- npm.
- Ruff optional.
- Pytest.
- Vitest optional.

## Deliberately excluded

- LangChain.
- Vector database.
- RAG.
- Kafka.
- Redis.
- Kubernetes.
- Firebase.
- Paid map APIs.
- Custom model training during the hackathon.
- Large local LLMs in the critical path.
