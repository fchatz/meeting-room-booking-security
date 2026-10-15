import os
import sqlite3, httpx, jwt
from datetime import datetime, timedelta, timezone
import reservation_service.main as reservation_service
from fastapi.testclient import TestClient

def test_create_reservation(tmp_path, monkeypatch):
    test_db = tmp_path / "reservations.db"
    con = sqlite3.connect(test_db)
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, room_id INTEGER NOT NULL, date TEXT NOT NULL, start_time TEXT NOT NULL, status TEXT NOT NULL)'
    )
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS unique_active_booking ON reservations (room_id, date, start_time) WHERE status = 'active'"
    )
    con.commit()
    con.close()
    monkeypatch.setattr(reservation_service, "DB_PATH", str(test_db))
    assert  reservation_service.create_reservation(1, 1, "2026-10-19", "10:00") == True
    assert reservation_service.create_reservation(2, 1, "2026-10-19", "10:00") == False
    assert reservation_service.create_reservation(2, 1, "2026-10-19", "10:30") == False
    assert reservation_service.create_reservation(2, 1, "2026-10-19", "11:00") == True
    con = sqlite3.connect(test_db)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM reservations")
    result = cur.fetchone()[0]
    assert result == 2
    con.close()

def test_reservation_required_authentication():
    client = TestClient(reservation_service.app)
    response = client.post("/reservations", json={
        "room_id": 1,
        "date": "2026-10-19",
        "start_time": "14:00"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization Header"

def test_reservation_invalid_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-only-secret-key-for-jwt-testing-i-need-more-bytes-for-HS256")
    client = TestClient(reservation_service.app)
    headers = {"Authorization": "Bearer invalid.token.value"}
    response = client.post("/reservations", json={
        "room_id": 1,
        "date": "2026-10-19",
        "start_time": "14:00"
    }, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or Expired token"

def test_invalid_schedule(monkeypatch):
    monkeypatch.setattr(
        reservation_service.httpx,
        "post",
        lambda *args, **kwargs: httpx.Response(200, json={"valid": False})
    )
    result = reservation_service.check_schedule("2026-10-17", "11:00")
    assert result == False

def test_scheduling_service_unavailable(monkeypatch):
    def fail_post(*args, **kwargs):
        raise httpx.ConnectError("Scheduling Service unavailable")
    monkeypatch.setattr(
        reservation_service.httpx,
        "post",
        fail_post
    )
    result = reservation_service.check_schedule("2026-10-19", "11:00")
    assert result == False

def test_read_reservation_authorization(tmp_path, monkeypatch):
    test_db = tmp_path / "reservations.db"
    con = sqlite3.connect(test_db)
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, room_id INTEGER NOT NULL, date TEXT NOT NULL, start_time TEXT NOT NULL, status TEXT NOT NULL)'
    )
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS unique_active_booking ON reservations (room_id, date, start_time) WHERE status = 'active'"
    )
    con.commit()
    con.close()
    monkeypatch.setattr(reservation_service, "DB_PATH", str(test_db))
    reservation_service.create_reservation(1, 1, "2026-10-19", "10:00")
    # secret_key = "test-only-secret-key-for-jwt-testing-i-need-more-bytes-for-HS256"
    monkeypatch.setenv("JWT_SECRET_KEY", "test-only-secret-key-for-jwt-testing-i-need-more-bytes-for-HS256")
    alice_payload = {
        "sub": "1",
        "role": "user",
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    bob_payload = {
        "sub": "2",
        "role": "user",
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    admin_payload = {
        "sub": "3",
        "role": "admin",
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    alice_token = jwt.encode(alice_payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    bob_token = jwt.encode(bob_payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    admin_token = jwt.encode(admin_payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    client = TestClient(reservation_service.app)
    alice_headers = {
        "Authorization": f"Bearer {alice_token}",
    }
    response = client.get("/reservations/1", headers=alice_headers)
    assert response.status_code == 200
    assert response.json()["user_id"] == 1
    bob_headers = {
        "Authorization": f"Bearer {bob_token}",
    }
    response = client.get("/reservations/1", headers=bob_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Access Denied"
    admin_headers = {
        "Authorization": f"Bearer {admin_token}",
    }
    response = client.get("/reservations/1", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["user_id"] == 1
    response = client.get("/reservations/999", headers=alice_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"
    response = client.get("/reservations/999", headers=bob_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"
    response = client.get("/reservations/999", headers=admin_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"

def test_read_reservation_requires_authentication():
    client = TestClient(reservation_service.app)
    response = client.get("/reservations/1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization Header"

def test_cancel_reservation_authorization(tmp_path, monkeypatch):
    test_db = tmp_path / "reservations.db"
    con = sqlite3.connect(test_db)
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, room_id INTEGER NOT NULL, date TEXT NOT NULL, start_time TEXT NOT NULL, status TEXT NOT NULL)'
    )
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS unique_active_booking ON reservations (room_id, date, start_time) WHERE status = 'active'"
    )
    con.commit()
    con.close()
    monkeypatch.setattr(reservation_service, "DB_PATH", str(test_db))
    reservation_service.create_reservation(1, 1, "2026-10-19", "10:00")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-only-secret-key-for-jwt-testing-i-need-more-bytes-for-HS256")
    alice_payload = {
        "sub": "1",
        "role": "user",
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    bob_payload = {
        "sub": "2",
        "role": "user",
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    admin_payload = {
        "sub": "3",
        "role": "admin",
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    alice_token = jwt.encode(alice_payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    bob_token = jwt.encode(bob_payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    admin_token = jwt.encode(admin_payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    client = TestClient(reservation_service.app)
    bob_headers = {
        "Authorization": f"Bearer {bob_token}",
    }
    response = client.delete("/reservations/1", headers=bob_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Access Denied"
    status = reservation_service.get_reservation(1)
    assert status[5] == "active"
    alice_headers = {
        "Authorization": f"Bearer {alice_token}",
    }
    response = client.delete("/reservations/1", headers=alice_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Reservation cancelled successfully"
    status = reservation_service.get_reservation(1)
    assert status[5] == "cancelled"
    response = client.delete("/reservations/1", headers=alice_headers)
    assert response.status_code == 409
    assert response.json()["detail"] == "Reservation already cancelled"
    reservation_service.create_reservation(2, 2, "2026-10-19", "11:00")
    admin_headers = {
        "Authorization": f"Bearer {admin_token}",
    }
    response = client.delete("/reservations/2", headers=admin_headers)
    assert response.status_code == 200
    status = reservation_service.get_reservation(2)
    assert status[5] == "cancelled"
    response = client.delete("/reservations/999", headers=alice_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"


def test_cancel_reservation_requires_authentication(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-only-secret-key-for-jwt-testing-i-need-more-bytes-for-HS256")
    client = TestClient(reservation_service.app)
    response = client.delete("/reservations/999")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization Header"
    alice_payload = {
        "sub": "1",
        "role": "user",
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=30),
    }
    alice_token = jwt.encode(alice_payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
    alice_headers = {
        "Authorization": f"Bearer {alice_token}",
    }
    response = client.delete("/reservations/1", headers=alice_headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or Expired token"
