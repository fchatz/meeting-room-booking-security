import sqlite3
from pwdlib import PasswordHash

users = [
    ("alice", "AlicePass123!", "user"),
    ("bob", "BobPass123!", "user"),
    ("admin", "AdminPass123!", "admin")
]

password_hasher = PasswordHash.recommended()

con = sqlite3.connect("application_api/auth.db")
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL)')
for username, password, role in users:
    hashed_password = password_hasher.hash(password)
    cur.execute('INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                (username, hashed_password, role))
con.commit()
con.close()