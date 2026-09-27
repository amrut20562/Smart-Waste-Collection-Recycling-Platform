from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from app.db import get_db
from app.schemas.vision import VisionClassifyResponse
from app.services.vision_service import VisionService
from app.models.waste_scan import WasteScan

router = APIRouter()

@router.post("/vision/classify", response_model=VisionClassifyResponse)
async def classify_waste(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "INVALID_IMAGE_TYPE", "message": "Uploaded file is not a valid image format."}}
        )

    try:
        contents = await image.read()
        result = VisionService.classify_image(contents)

        # Record scan in database for tracking
        scan_record = WasteScan(
            primary_category=result["category"],
            source=result["source"],
            score=result["score"],
            detections_json=json.dumps(result["detections"])
        )
        db.add(scan_record)
        db.commit()

        return result
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "IMAGE_PROCESSING_ERROR", "message": str(e)}}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": {"code": "VISION_SERVICE_ERROR", "message": f"Inference pipeline failure: {str(e)}"}}
        )
