"""
Sample Application - BEFORE Security Review
CodeAlpha Cyber Security Internship - Task 3

This is a small, intentionally insecure Flask-style login/user app used
as the subject of the secure coding review. Vulnerabilities are labeled
inline with [VULN-x] tags that map to findings.md.
"""

import sqlite3

# [VULN-1] Hardcoded credentials / secret key
SECRET_KEY = "admin123"
DB_PASSWORD = "root_password_2024"

conn = sqlite3.connect("users.db")
cursor = conn.cursor()


def login(username, password):
    # [VULN-2] SQL Injection - user input directly concatenated into query
    query = "SELECT * FROM users WHERE username = '" + username + \
             "' AND password = '" + password + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    return result is not None


def save_password(username, plain_password):
    # [VULN-3] Storing passwords in plain text, no hashing/encryption
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, plain_password)
    )
    conn.commit()


def read_user_file(filename):
    # [VULN-4] No input validation - path traversal possible
    # e.g. filename = "../../etc/passwd"
    with open(filename, "r") as f:
        return f.read()


def debug_log(data):
    # [VULN-5] Sensitive data printed to logs/console
    print(f"[DEBUG] User data: {data}")
