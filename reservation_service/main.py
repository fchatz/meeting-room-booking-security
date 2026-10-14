from fastapi import FastAPI, HTTPException, Header, Depends
import sqlite3, httpx
from datetime import datetime, timedelta
import jwt, os
from pydantic import BaseModel, Field
app = FastAPI()
DB_PATH = "reservation_service/reservations.db"

@app.get("/health")
async def root():
    return {"status": "ok"}


def get_reservation(reservation_id):
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute(
        'SELECT id, user_id, room_id, date, start_time, status FROM reservations WHERE id = ?',
        (reservation_id,)
    )
    reservation = cur.fetchone()
    con.close()
    return reservation

def create_reservation(user_id, room_id, date, start_time):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute("BEGIN IMMEDIATE")
        cur.execute(
            "SELECT start_time FROM reservations WHERE room_id = ? AND date = ? AND status = 'active'",
            (room_id, date)
        )
        existing_reservations = cur.fetchall()
        requested_start = datetime.strptime(start_time, "%H:%M")
        requested_end = requested_start + timedelta(hours=1)
        for existing in existing_reservations:
            existing_start = datetime.strptime(existing[0], "%H:%M")
            existing_end = existing_start + timedelta(hours=1)
            if requested_start < existing_end and existing_start < requested_end:
                con.rollback()
                return False
        cur.execute(
            "INSERT INTO reservations (user_id, room_id, date, start_time, status) VALUES (?, ?, ?, ?, 'active')",
            (user_id, room_id, date, start_time)
        )
        con.commit()
        return True
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def verify_access_token(token):
    key = os.environ["JWT_SECRET_KEY"]
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["HS256"],
            audience="meeting-room-booking",
            issuer="application-api",
            options={"require": ["sub", "role", "iss", "aud", "exp"]}
        )
        if payload["role"] not in ["user", "admin"]:
            raise HTTPException(status_code=401, detail="Invalid or Expired token")
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

class BookingRequest(BaseModel):
    room_id: int = Field(ge=1, le=3)
    date: str
    start_time: str

def get_current_user(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")
    scheme, seperator, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not seperator or not token:
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")
    verified_payload = verify_access_token(token)
    return verified_payload

@app.post("/reservations")
def book_reservation(request: BookingRequest, current_user = Depends(get_current_user)):
    check = check_schedule(request.date, request.start_time)
    if check is False:
        raise HTTPException(status_code=400, detail="Invalid booking schedule")
    user_id = int(current_user["sub"])
    reservation_flag = create_reservation(user_id, request.room_id, request.date, request.start_time)
    if reservation_flag is False:
        raise HTTPException(status_code=409, detail="Room is already booked")
    return {"message": "Reservation created successfully"}

def check_schedule(date, start_time):
    try:
        response = httpx.post(
            "http://127.0.0.1:8002/validate",
            json={
                "date_string": date,
                "start_time": start_time
            },
            timeout=5.0
        )
    except httpx.RequestError:
        return False
    if response.status_code != 200:
        return False

    try:
        data = response.json()
    except ValueError:
        return False
    if not isinstance(data, dict):
        return False
    return data.get("valid") is True