import sqlite3, httpx
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