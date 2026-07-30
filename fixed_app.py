"""
Sample Application - AFTER Security Review (Remediated)
CodeAlpha Cyber Security Internship - Task 3

Same functionality as vulnerable_app.py, rewritten with fixes for each
labeled [VULN-x] finding. See findings.md for the full explanation.
"""

import sqlite3
import os
import bcrypt

# [FIX-1] Secrets loaded from environment variables, not hardcoded
SECRET_KEY = os.environ.get("APP_SECRET_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()


def login(username, password):
    # [FIX-2] Parameterized query prevents SQL injection
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    if result is None:
        return False

    stored_hash = result[1]  # assuming password hash stored in column 1
    # [FIX-3] Compare against bcrypt hash, never store/compare plain text
    return bcrypt.checkpw(password.encode(), stored_hash)


def save_password(username, plain_password):
    # [FIX-3] Hash password with bcrypt before storing
    hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed)
    )
    conn.commit()


# [FIX-4] Whitelist of files that are safe to read
ALLOWED_FILES = {"readme.txt", "notes.txt"}


def read_user_file(filename):
    # [FIX-4] Validate input, block path traversal
    if filename not in ALLOWED_FILES:
        raise ValueError("Access to this file is not permitted.")
    with open(filename, "r") as f:
        return f.read()


def debug_log(data):
    # [FIX-5] Mask sensitive fields before logging
    safe_data = {k: ("***" if k.lower() in ("password", "secret") else v)
                 for k, v in data.items()}
    print(f"[DEBUG] User data: {safe_data}")
