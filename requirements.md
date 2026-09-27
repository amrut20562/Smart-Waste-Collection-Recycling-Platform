# Required Packages

## Backend requirements.txt

Pin versions after selecting a tested environment. Do not use unconstrained `latest` installs in the final lock/requirements file.

Required packages:

- fastapi
- uvicorn[standard]
- sqlalchemy
- pydantic
- pydantic-settings
- python-multipart
- python-dotenv
- ultralytics
- torch
- torchvision
- transformers
- pillow
- numpy
- scikit-learn
- ortools
- pytest
- httpx

Optional only if needed:

- shapely
- pytest-asyncio

## Frontend packages

Required:

- react
- react-dom
- react-router-dom
- typescript
- vite
- tailwindcss
- lucide-react
- leaflet
- react-leaflet
- recharts

Do not add UI libraries unless the same requirement cannot be met cleanly with the selected stack.
