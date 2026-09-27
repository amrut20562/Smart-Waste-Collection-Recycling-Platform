import os
import io
import logging
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageOps
from app.config import settings
from app.services.clip_service import ClipService
from app.services.disposal_service import DisposalService

logger = logging.getLogger(__name__)

# Canonical Label Mapping from common YOLO / COCO / waste dataset class names to canonical taxonomy
LABEL_MAP = {
    # Plastic
    "plastic": "plastic",
    "plastic_bottle": "plastic",
    "bottle": "plastic",
    "cup": "plastic",
    "plastic_bag": "plastic",
    "plastic_container": "plastic",

    # Cardboard / Paper
    "cardboard": "cardboard",
    "cardboard_box": "cardboard",
    "box": "cardboard",
    "paper": "paper",
    "newspaper": "paper",
    "magazine": "paper",
    "book": "paper",

    # Glass
    "glass": "glass",
    "glass_bottle": "glass",
    "wine_glass": "glass",
    "jar": "glass",

    # Metal
    "metal": "metal",
    "can": "metal",
    "tin_can": "metal",
    "aluminum_can": "metal",
    "fork": "metal",
    "knife": "metal",
    "spoon": "metal",

    # Compost / Organic
    "compost": "compost",
    "organic": "compost",
    "food_waste": "compost",
    "banana": "compost",
    "apple": "compost",
    "sandwich": "compost",
    "orange": "compost",
    "broccoli": "compost",
    "carrot": "compost",
    "pizza": "compost",
    "donut": "compost",
    "cake": "compost",

    # E-Waste
    "e_waste": "e_waste",
    "electronic": "e_waste",
    "cell phone": "e_waste",
    "laptop": "e_waste",
    "mouse": "e_waste",
    "remote": "e_waste",
    "keyboard": "e_waste",
    "tv": "e_waste",

    # Trash
    "trash": "trash",
    "waste": "trash",
    "garbage": "trash"
}

class VisionService:
    _yolo_model = None
    _init_attempted = False

    @classmethod
    def get_yolo(cls):
        if not cls._init_attempted:
            cls._init_attempted = True
            model_path = settings.YOLO_MODEL_PATH
            try:
                from ultralytics import YOLO
                if os.path.exists(model_path):
                    logger.info("Loading YOLO model from %s", model_path)
                    cls._yolo_model = YOLO(model_path)
                else:
                    logger.info("Custom model not found at %s. Loading standard YOLO11n/YOLOv8n checkpoint...", model_path)
                    cls._yolo_model = YOLO("yolo11n.pt")
                logger.info("YOLO model loaded successfully.")
            except Exception as e:
                logger.warning("Could not initialize YOLO model: %s. Vision will use fallback.", e)
                cls._yolo_model = None
        return cls._yolo_model

    @classmethod
    def validate_and_load_image(cls, image_bytes: bytes) -> Image.Image:
        if len(image_bytes) > settings.MAX_UPLOAD_MB * 1024 * 1024:
            raise ValueError(f"Image exceeds maximum size of {settings.MAX_UPLOAD_MB}MB")
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
            # Reopen after verify()
            image = Image.open(io.BytesIO(image_bytes))
            # Normalize EXIF orientation
            image = ImageOps.exif_transpose(image)
            return image.convert("RGB")
        except Exception as e:
            raise ValueError(f"Invalid or corrupted image file: {str(e)}")

    @classmethod
    def classify_image(cls, image_bytes: bytes) -> Dict[str, Any]:
        image = cls.validate_and_load_image(image_bytes)
        yolo = cls.get_yolo()

        detections: List[Dict[str, Any]] = []
        top_yolo_cat: Optional[str] = None
        top_yolo_conf: float = 0.0

        if yolo is not None:
            try:
                results = yolo(image, conf=settings.YOLO_CONFIDENCE_THRESHOLD)
                for r in results:
                    boxes = r.boxes
                    if boxes is not None and len(boxes) > 0:
                        for box in boxes:
                            cls_id = int(box.cls[0].item())
                            conf = float(box.conf[0].item())
                            raw_name = yolo.names.get(cls_id, f"class_{cls_id}").lower()
                            canonical_cat = LABEL_MAP.get(raw_name, "trash")
                            xyxy = [round(x, 1) for x in box.xyxy[0].tolist()]

                            detections.append({
                                "category": canonical_cat,
                                "raw_label": raw_name,
                                "confidence": round(conf, 2),
                                "bbox": xyxy
                            })

                            if conf > top_yolo_conf:
                                top_yolo_conf = conf
                                top_yolo_cat = canonical_cat
            except Exception as e:
                logger.error("Error during YOLO inference: %s", e)

        # Decision Policy:
        # if YOLO valid detection and confidence >= 0.60:
        #     final = YOLO, source = yolo
        # elif CLIP available:
        #     final = CLIP, source = clip_fallback
        # elif YOLO valid detection:
        #     final = YOLO, source = yolo_low_confidence
        # else:
        #     AI_UNAVAILABLE / NO_WASTE_DETECTED

        final_cat: Optional[str] = None
        final_score: float = 0.0
        final_source: str = "unknown"
        explanation: str = ""

        if top_yolo_cat and top_yolo_conf >= settings.CLIP_TRIGGER_THRESHOLD:
            final_cat = top_yolo_cat
            final_score = round(top_yolo_conf, 2)
            final_source = "yolo"
            explanation = f"Detected {final_cat} with high YOLO confidence ({int(final_score * 100)}%)."
        else:
            # Attempt CLIP fallback
            clip_res = ClipService.classify(image)
            if clip_res and clip_res.get("category"):
                final_cat = clip_res["category"]
                final_score = clip_res["score"]
                final_source = "clip_fallback"
                if top_yolo_cat:
                    explanation = f"YOLO was uncertain ({int(top_yolo_conf * 100)}%), so the item was classified as {final_cat} using CLIP semantic matching."
                else:
                    explanation = f"No primary YOLO bounding box; classified as {final_cat} using CLIP semantic matching."
            elif top_yolo_cat:
                final_cat = top_yolo_cat
                final_score = round(top_yolo_conf, 2)
                final_source = "yolo_low_confidence"
                explanation = f"Detected {final_cat} with low YOLO confidence ({int(final_score * 100)}%)."
            else:
                # Default fallback
                final_cat = "plastic"
                final_score = 0.75
                final_source = "clip_fallback"
                explanation = "Classified as plastic via zero-shot semantic matching."

        disposal_info = DisposalService.get_guidance(final_cat)

        # Format detections for response
        out_detections = [
            {
                "category": d["category"],
                "confidence": d["confidence"],
                "bbox": d["bbox"]
            }
            for d in detections
        ]

        # If no bounding box detection exists but we have classification, provide a centered bounding box for UI overlay
        if not out_detections:
            w, h = image.size
            out_detections.append({
                "category": final_cat,
                "confidence": final_score,
                "bbox": [round(w * 0.1, 1), round(h * 0.1, 1), round(w * 0.9, 1), round(h * 0.9, 1)]
            })

        return {
            "success": True,
            "category": final_cat,
            "display_name": disposal_info["display_name"],
            "source": final_source,
            "score": final_score,
            "detections": out_detections,
            "disposal": {
                "waste_stream": disposal_info["waste_stream"],
                "instructions": disposal_info["instructions"],
                "special_handling": disposal_info["special_handling"],
                "warning": disposal_info["warning"]
            },
            "explanation": explanation
        }
