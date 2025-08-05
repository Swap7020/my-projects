import sqlite3

DB = 'data/bookings.db'

def create_booking_table():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            location TEXT,
            date TEXT,
            time TEXT,
            duration INTEGER,
            vehicle_type TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_booking(user, location, date, time, duration, vehicle_type):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        INSERT INTO bookings (user, location, date, time, duration, vehicle_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user, location, date, time, duration, vehicle_type, "Pending"))
    conn.commit()
    conn.close()

def get_all_bookings():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_bookings(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE user=?", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_booking_status(booking_id, new_status):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE bookings SET status=? WHERE id=?", (new_status, booking_id))
    conn.commit()
    conn.close()

