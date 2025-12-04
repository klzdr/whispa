# models.py
import hashlib
import os
from database import get_connection

# -----------------------------
# Generate hashed password
# -----------------------------
def hash_password(password):
    salt = os.urandom(16).hex()  # generate random salt
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def verify_password(password, stored_hash, stored_salt):
    hashed = hashlib.sha256((password + stored_salt).encode()).hexdigest()
    return hashed == stored_hash
# -----------------------------
# Create a new user (FIXED)
# -----------------------------
def create_user(username, email, password): # FIX: Added 'email' to parameters
    hashed, salt = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            # FIX: Added 'email' to column list and value placeholders
            "INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
            (username, email, hashed, salt) # FIX: Added 'email' to values tuple
        )
        conn.commit()
        return True, "User created successfully."
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "Username or Email already taken."
        return False, str(e)
    finally:
        conn.close()

# -----------------------------
# Authenticate user
# -----------------------------
def authenticate(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    success = False
    message = "Login failed."

    try:
        cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row is None:
            message = "User not found."
        else:
            stored_hash, stored_salt = row

            if verify_password(password, stored_hash, stored_salt):
                success = True
                message = "Login successful."
            else:
                message = "Incorrect password."

    except Exception as e:
        message = f"Database error during authentication: {e}"

    finally:
        # Guarantee connection closure
        conn.close()

    return success, message
