
from fastapi.testclient import TestClient
from scheduling_service.main import app


def test_valid_booking_request():
    client = TestClient(app)
    response = client.post("/validate", json={
        "date_string": "2026-10-14",
        "start_time": "10:00"
    })
    assert response.status_code == 200
    assert response.json() == {"valid": True}

def test_invalid_date_request():
    client = TestClient(app)
    response = client.post("/validate", json={
        "date_string": "test",
        "start_time": "10:00"
    })
    assert response.status_code == 422