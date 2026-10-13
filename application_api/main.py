from fastapi import FastAPI
from pwdlib import PasswordHash
import sqlite3
import jwt
import os
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from fastapi import HTTPException
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