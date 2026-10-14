import sqlite3

con = sqlite3.connect("reservation_service/reservations.db")
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, room_id INTEGER NOT NULL, date TEXT NOT NULL, start_time TEXT NOT NULL, status TEXT NOT NULL)')
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS unique_active_booking ON reservations (room_id, date, start_time) WHERE status = 'active'")
con.commit()
con.close()