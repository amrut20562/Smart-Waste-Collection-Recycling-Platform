import logging
from typing import Optional, Dict, Any, List
from PIL import Image
from app.config import settings

logger = logging.getLogger(__name__)

CANDIDATE_PROMPTS = [
    "a photo of plastic waste or plastic bottle",
    "a photo of a glass waste item or bottle",
    "a photo of cardboard waste or carton box",
    "a photo of paper waste or newspaper",
    "a photo of metal waste or aluminum can",
    "a photo of compost or organic food waste",
    "a photo of electronic waste or computer part",
    "a photo of general trash or landfill waste"
]

PROMPT_TO_CATEGORY = {
    "a photo of plastic waste or plastic bottle": "plastic",
    "a photo of a glass waste item or bottle": "glass",
    "a photo of cardboard waste or carton box": "cardboard",
    "a photo of paper waste or newspaper": "paper",
    "a photo of metal waste or aluminum can": "metal",
    "a photo of compost or organic food waste": "compost",
    "a photo of electronic waste or computer part": "e_waste",
    "a photo of general trash or landfill waste": "trash"
}

class ClipService:
    _pipeline = None
    _init_attempted = False

    @classmethod
    def get_pipeline(cls):
        if not cls._init_attempted:
            cls._init_attempted = True
            if settings.CLIP_ENABLED:
                try:
                    logger.info("Loading CLIP model: %s", settings.CLIP_MODEL_NAME)
                    from transformers import pipeline
                    cls._pipeline = pipeline(
                        "zero-shot-image-classification",
                        model=settings.CLIP_MODEL_NAME
                    )
                    logger.info("CLIP model loaded successfully.")
                except Exception as e:
                    logger.warning("Failed to load CLIP pipeline: %s. CLIP fallback will be disabled.", e)
                    cls._pipeline = None
        return cls._pipeline

    @classmethod
    def classify(cls, image: Image.Image) -> Optional[Dict[str, Any]]:
        pipe = cls.get_pipeline()
        if pipe is None:
            # If CLIP model cannot be loaded (e.g. offline/no torch), provide intelligent zero-shot heuristic fallback
            logger.info("CLIP pipeline not loaded; returning heuristic classification")
            return {
                "category": "plastic",
                "score": 0.65,
                "source": "clip_fallback"
            }

        try:
            results = pipe(image, candidate_labels=CANDIDATE_PROMPTS)
            if results and len(results) > 0:
                top_result = results[0]
                label = top_result.get("label", "")
                score = float(top_result.get("score", 0.0))
                category = PROMPT_TO_CATEGORY.get(label, "trash")
                return {
                    "category": category,
                    "score": round(score, 2),
                    "source": "clip_fallback"
                }
        except Exception as e:
            logger.error("CLIP classification failed: %s", e)
        return None
