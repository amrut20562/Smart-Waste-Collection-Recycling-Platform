from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./smart_waste.db"
    YOLO_MODEL_PATH: str = "./models/waste_yolo.pt"
    YOLO_CONFIDENCE_THRESHOLD: float = 0.45
    CLIP_ENABLED: bool = True
    CLIP_MODEL_NAME: str = "openai/clip-vit-base-patch32"
    CLIP_TRIGGER_THRESHOLD: float = 0.60
    DBSCAN_EPS_METERS: int = 750
    DBSCAN_MIN_SAMPLES: int = 2
    ROUTE_SOLVER_SECONDS: int = 2
    ROAD_FACTOR: float = 1.20
    MAX_UPLOAD_MB: int = 8

settings = Settings()
