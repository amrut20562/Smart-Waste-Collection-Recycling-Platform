# AI Pipeline Specification

## 1. Canonical waste taxonomy

The initial taxonomy is:

- cardboard
- compost
- glass
- metal
- paper
- plastic
- trash
- e_waste (optional only if the selected checkpoint supports it)

The backend must normalize model labels through a mapping table instead of depending on exact checkpoint class names.

Example:

```python
LABEL_MAP = {
    "cardboard_box": "cardboard",
    "cardboard": "cardboard",
    "plastic_bottle": "plastic",
    "plastic": "plastic",
    "glass": "glass",
    "metal": "metal",
    "paper": "paper",
    "organic": "compost",
    "food_waste": "compost",
    "trash": "trash",
}
```

Do not assume the selected checkpoint uses these exact labels. Load class names from the checkpoint and maintain an explicit mapping in configuration.

## 2. YOLO inference contract

Input:

- RGB image.
- Maximum accepted upload: 8 MB.
- Reject non-image files.
- Normalize EXIF orientation.

Output per detection:

```json
{
  "raw_label": "plastic_bottle",
  "category": "plastic",
  "confidence": 0.94,
  "bbox": [x1, y1, x2, y2]
}
```

Use the best valid detection for single-item mode. If multiple detections exist, return all detections and derive a `primary_category` using the highest confidence valid detection.

## 3. CLIP fallback

Use zero-shot prompts, not generic class words only.

Suggested prompts:

- `a photo of plastic waste`
- `a photo of a glass waste item`
- `a photo of cardboard waste`
- `a photo of paper waste`
- `a photo of metal waste`
- `a photo of compost or food waste`
- `a photo of electronic waste`
- `a photo of general trash`

Run CLIP only when:

- YOLO produced zero valid detections; OR
- best valid YOLO confidence < 0.60.

Return:

```json
{
  "category": "plastic",
  "score": 0.71,
  "source": "clip_fallback"
}
```

Call this `score`, not `confidence`, because CLIP similarity is not automatically a calibrated probability.

## 4. Decision policy

```text
if YOLO valid detection and confidence >= 0.60:
    final = YOLO
    source = yolo
elif CLIP available:
    final = CLIP
    source = clip_fallback
elif YOLO valid detection:
    final = YOLO
    source = yolo_low_confidence
else:
    return AI_UNAVAILABLE / NO_WASTE_DETECTED
```

Do not average YOLO and CLIP scores mathematically.

## 5. Explainability

Return an explanation such as:

`Detected plastic with high YOLO confidence.`

or

`YOLO was uncertain, so the image was classified using CLIP semantic matching.`

## 6. Disposal engine

The disposal engine is deterministic. Create a local dictionary/table keyed by canonical category.

Example fields:

```text
category
waste_stream
instructions
special_handling
pickup_supported
warning
```

Never generate municipal policy or safety instructions from an LLM.

## 7. LLM exclusion

An LLM is not part of the required MVP. Add one only after the vision and routing pipelines are stable and only for explanation/chat, never as the source of operational truth.
