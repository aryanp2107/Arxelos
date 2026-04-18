"""
Smoke tests for Arxelos health endpoints.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["platform"] == "Arxelos"


def test_model_status():
    response = client.get("/health/models")
    assert response.status_code == 200
    data = response.json()
    assert "tumor_classifier" in data
    assert "virtual_lesions" in data
    assert "medical_rag" in data


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "Arxelos"
    assert data["status"] == "operational"
