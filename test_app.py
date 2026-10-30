from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction():
    data = {
        "study_hours": 8,
        "attendance": 90,
        "previous_score": 80,
        "assignments_completed": 9
    }

    response = client.post("/predict", json=data)

    assert response.status_code == 200
    assert response.json()["result"] == "Pass"


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
