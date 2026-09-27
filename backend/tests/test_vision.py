import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.services.disposal_service import DisposalService

client = TestClient(app)

def create_test_image_bytes(color=(255, 0, 0), size=(200, 200)) -> bytes:
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_disposal_knowledge_base():
    guidance = DisposalService.get_guidance("plastic")
    assert guidance["display_name"] == "Plastic"
    assert guidance["waste_stream"] == "Dry Recyclable"
    assert len(guidance["instructions"]) > 0

    guidance_e = DisposalService.get_guidance("e_waste")
    assert guidance_e["special_handling"] is True

def test_vision_valid_image():
    img_bytes = create_test_image_bytes()
    response = client.post(
        "/api/v1/vision/classify",
        files={"image": ("test.jpg", img_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "category" in data
    assert "score" in data
    assert "source" in data
    assert "disposal" in data
    assert len(data["detections"]) > 0

def test_vision_invalid_file():
    response = client.post(
        "/api/v1/vision/classify",
        files={"image": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 400
