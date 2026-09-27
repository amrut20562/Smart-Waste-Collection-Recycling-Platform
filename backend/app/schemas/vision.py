from pydantic import BaseModel
from typing import List, Optional

class BoundingBox(BaseModel):
    category: str
    confidence: float
    bbox: List[float]

class DisposalInfo(BaseModel):
    waste_stream: str
    instructions: List[str]
    special_handling: bool = False
    warning: Optional[str] = None

class VisionClassifyResponse(BaseModel):
    success: bool
    category: str
    display_name: str
    source: str
    score: float
    detections: List[BoundingBox]
    disposal: DisposalInfo
    explanation: Optional[str] = None
