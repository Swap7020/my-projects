import sqlite3
import hashlib

DB_NAME = "users.db"

def create_user_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_user(username, password, role, contact):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role, contact) VALUES (?, ?, ?, ?)',
              (username, password, role, contact))
    conn.commit()
    conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_pw(password)))
    result = c.fetchone()
    conn.close()
    return result

def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_user_contact(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT contact FROM users WHERE username = ?', (username,))
    contact = c.fetchone()
    conn.close()
    return contact[0] if contact else "Not available"
