from fastapi import FastAPI,HTTPException, Header
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
import sqlite3, jwt, os, httpx
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
app = FastAPI()
password_hasher = PasswordHash.recommended()
@app.get("/health")
async def root():
    return {"status": "ok"}


def get_user(username):
    con = sqlite3.connect(
        "file:application_api/auth.db?mode=ro",
        uri=True
    )
    cur = con.cursor()
    cur.execute(
        'SELECT id, username, password_hash, role FROM users WHERE username = ?',
        (username,)
    )
    user = cur.fetchone()
    con.close()
    return user

def authenticate_user(username, password):
    user = get_user(username)
    if user is None:
        return None

    pass_verification = password_hasher.verify(password, user[2])

    if not pass_verification:
        return None

    return user

def create_access_token(user):
    key = os.environ["JWT_SECRET_KEY"]
    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub": str(user[0]),
        "role": user[3],
        "iss": "application-api",
        "aud": "meeting-room-booking",
        "exp": expiration
    }
    signed = jwt.encode(payload, key, algorithm="HS256")
    return signed

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}

class BookingRequest(BaseModel):
    room_id: int = Field(ge=1, le=3)
    date: str
    start_time: str

@app.post("/reservations")
def book_reservation(request: BookingRequest, authorization: str | None = Header(default= None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")
    try:
        response = httpx.post(
            "http://127.0.0.1:8001/reservations",
            json=request.model_dump(),
            headers={"Authorization": authorization},
            timeout=5.0
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Reservation Service Unavailable")
    return JSONResponse(status_code=response.status_code, content=response.json())

@app.get("/reservations/{reservation_id}")
def read_reservation(reservation_id: int, authorization: str | None = Header(default= None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")
    try:
        response = httpx.get(
            url=f"http://127.0.0.1:8001/reservations/{reservation_id}",
            headers={"Authorization": authorization},
            timeout=5.0
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Reservation Service Unavailable")
    return JSONResponse(status_code=response.status_code, content=response.json())

@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, authorization: str | None = Header(default= None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")
    try:
        response = httpx.delete(
            url=f"http://127.0.0.1:8001/reservations/{reservation_id}",
            headers={"Authorization": authorization},
            timeout=5.0
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Reservation Service Unavailable")
    return JSONResponse(status_code=response.status_code, content=response.json())

@app.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: int, request: BookingRequest, authorization: str | None = Header(default= None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")
    try:
        response = httpx.put(
            url=f"http://127.0.0.1:8001/reservations/{reservation_id}",
            json=request.model_dump(),
            headers={"Authorization": authorization},
            timeout=5.0
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Reservation Service Unavailable")
    return JSONResponse(status_code=response.status_code, content=response.json())