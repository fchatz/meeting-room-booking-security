import os
from webbrowser import get

import httpx
from urllib3.util import url

import application_api.main as application_api
from fastapi.testclient import TestClient

def test_application_booking_coordination(monkeypatch):
    def mock_post(url, **kwargs):
        assert url == "http://127.0.0.1:8001/reservations"
        assert kwargs["headers"]["Authorization"] == "Bearer test-token"
        assert kwargs["json"]["room_id"] == 1
        assert kwargs["json"]["date"] == "2026-10-19"
        assert kwargs["json"]["start_time"] == "10:00"
        return httpx.Response(
            200,
            json={"message": "Reservation created successfully"}
        )
    monkeypatch.setattr(
        application_api.httpx,
        "post",
        mock_post
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.post("/reservations",headers=header , json={
        "room_id": 1,
        "date": "2026-10-19",
        "start_time": "10:00"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Reservation created successfully"

def test_application_booking_conflict(monkeypatch):
    monkeypatch.setattr(
        application_api.httpx,
        "post",
        lambda *args, **kwargs: httpx.Response(
            409,
            json={"detail": "Room is already booked"}
        )
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.post("/reservations",headers=header , json={
        "room_id": 1,
        "date": "2026-10-19",
        "start_time": "10:00"
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "Room is already booked"

def test_application_booking_service_unavailable(monkeypatch):
    def mock_post(*args, **kwargs):
        raise httpx.ConnectError("Reservation Service unavailable")

    monkeypatch.setattr(
        application_api.httpx,
        "post",
        mock_post
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.post("/reservations", headers=header, json={
        "room_id": 1,
        "date": "2026-10-19",
        "start_time": "10:00"
    })
    assert response.status_code == 503
    assert response.json()["detail"] == "Reservation Service Unavailable"

def test_application_get_coordination(monkeypatch):
    def mock_get(url, **kwargs):
        assert url == "http://127.0.0.1:8001/reservations/1"
        assert kwargs["headers"]["Authorization"] == "Bearer test-token"
        return httpx.Response(
           200,
           json={
                "id": 1,
                "user_id": 1,
                "room_id": 1,
                "date": "2026-10-19",
                "start_time": "10:00",
                "status": "active"
           }
       )
    monkeypatch.setattr(
        application_api.httpx,
        "get",
        mock_get
    )
    header = {
        "Authorization": "Bearer test-token"
    }
    client = TestClient(application_api.app)
    response = client.get("/reservations/1", headers=header)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["user_id"] == 1

def test_application_get_forbidden(monkeypatch):
    monkeypatch.setattr(
        application_api.httpx,
        "get",
        lambda *args, **kwargs: httpx.Response(
            403,
            json={"detail": "Access Denied"}
        )
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.get("/reservations/1", headers=header)
    assert response.status_code == 403
    assert response.json()["detail"] == "Access Denied"

def test_application_get_not_found(monkeypatch):
    monkeypatch.setattr(
        application_api.httpx,
        "get",
        lambda *args, **kwargs: httpx.Response(
            404,
            json={"detail": "Reservation not found"}
        )
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.get("/reservations/1", headers=header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"

def test_application_delete_coordination(monkeypatch):
    def mock_delete(url, **kwargs):
        assert url == "http://127.0.0.1:8001/reservations/1"
        assert kwargs["headers"]["Authorization"] == "Bearer test-token"
        return httpx.Response(
            200,
            json={"message": "Reservation cancelled successfully"}
        )
    monkeypatch.setattr(
        application_api.httpx,
        "delete",
        mock_delete
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.delete("/reservations/1", headers=header)
    assert response.status_code == 200
    assert response.json()["message"] == "Reservation cancelled successfully"

def test_application_delete_conflict(monkeypatch):
    monkeypatch.setattr(
        application_api.httpx,
        "delete",
        lambda *args, **kwargs: httpx.Response(
            409,
            json={"detail": "Reservation already cancelled"}
        )
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.delete("/reservations/1", headers=header)
    assert response.status_code == 409
    assert response.json()["detail"] == "Reservation already cancelled"

def test_application_put_coordination(monkeypatch):
    def mock_put(url, **kwargs):
        assert url == "http://127.0.0.1:8001/reservations/1"
        assert kwargs["headers"]["Authorization"] == "Bearer test-token"
        assert kwargs["json"]["room_id"] == 2
        assert kwargs["json"]["date"] == "2026-10-20"
        assert kwargs["json"]["start_time"] == "11:00"
        return httpx.Response(200, json={"message": "Reservation rescheduled successfully"})
    monkeypatch.setattr(
        application_api.httpx,
        "put",
        mock_put
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.put("/reservations/1", headers=header, json={
        "room_id": 2,
        "date": "2026-10-20",
        "start_time": "11:00",
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Reservation rescheduled successfully"

def test_application_put_conflict(monkeypatch):
    monkeypatch.setattr(
        application_api.httpx,
        "put",
        lambda url, **kwargs: httpx.Response(
            409,
            json={"detail": "Requested time slot is unavailable"}
        )
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.put("/reservations/1", headers=header, json={
        "room_id": 2,
        "date": "2026-10-20",
        "start_time": "11:00",
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "Requested time slot is unavailable"

def test_application_put_service_unavailable(monkeypatch):
    def mock_put(*args, **kwargs):
        raise httpx.ConnectError("Reservation Service unavailable")
    monkeypatch.setattr(
        application_api.httpx,
        "put",
        mock_put
    )
    client = TestClient(application_api.app)
    header = {
        "Authorization": "Bearer test-token"
    }
    response = client.put("/reservations/1", headers=header, json={
        "room_id": 2,
        "date": "2026-10-20",
        "start_time": "11:00",
    })
    assert response.status_code == 503
    assert response.json()["detail"] == "Reservation Service Unavailable"
