"""
Tests for the Brain Tumor Classifier API endpoints.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_tumor_info():
    """Model info endpoint should return metadata."""
    response = client.get("/api/v1/tumor/info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "Brain Tumor MRI Classifier"
    assert data["architecture"] == "Custom 30-layer Sequential CNN"
    assert data["input_size"] == "224x224x3"
    assert len(data["classes"]) == 4
    assert "glioma" in data["classes"]
    assert "notumor" in data["classes"]


def test_predict_no_model():
    """Predict should return 503 when model is not loaded."""
    # Create a minimal JPEG-like file
    import io
    from PIL import Image

    img = Image.new("RGB", (224, 224), color="gray")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    response = client.post(
        "/api/v1/tumor/predict",
        files={"file": ("test.jpg", buf, "image/jpeg")},
    )
    # Model won't be loaded in test env, so expect 503
    assert response.status_code == 503


def test_predict_invalid_file_type():
    """Predict should reject non-image files."""
    response = client.post(
        "/api/v1/tumor/predict",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_predict_empty_file():
    """Predict should reject empty files."""
    response = client.post(
        "/api/v1/tumor/predict",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
    )
    assert response.status_code == 400
