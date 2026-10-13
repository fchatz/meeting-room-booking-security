from fastapi.testclient import TestClient
from application_api.main import app

def test_valid_login(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-only-secret-key-for-jwt-testing-i-need-more-bytes-for-HS256")
    client = TestClient(app)
    response = client.post("/login", json={
        "username": "alice",
        "password": "AlicePass123!"
    })
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"

def test_invalid_password():
    client = TestClient(app)
    response = client.post("/login", json={
        "username": "alice",
        "password": "WrongPassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

def test_unknown_user():
    client = TestClient(app)
    response = client.post("/login", json={
        "username": "unknown",
        "password": "Password123"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
