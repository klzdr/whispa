# backend/database.py
import sqlite3
import hashlib
import os

DB_PATH = "backend/users.db"  # Adjust path to be relative to Whispa folder

# -----------------------------
# Connection
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# -----------------------------
# Table setup
# -----------------------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL, 
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

create_tables()

# -----------------------------
# User functions
# -----------------------------
def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, email, password):
    salt = os.urandom(16).hex()
    pw_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
                   (username, email, pw_hash, salt))
    conn.commit()
    conn.close()

def verify_password(password, pw_hash, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest() == pw_hash
