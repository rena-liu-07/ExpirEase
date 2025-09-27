import sqlite3
import hashlib
from datetime import datetime
import os

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

# 初始化 user 表
conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT,
    created_at TEXT
)
""")
conn.commit()
conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    password_hash = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO user (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, created_at)
        )
        conn.commit()
        print(f"User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
    conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute(
        "SELECT id FROM user WHERE username=? AND password=?",
        (username, password_hash)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        print(f"User '{username}' logged in.")
        return row[0]  # 返回 user_id
    else:
        print("Login failed.")
        return None

if __name__ == "__main__":
    while True:
        print("\n--- Login System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            register_user(username, email, password)
        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            login_user(username, password)
        elif choice == "3":
            break
        else:
            print("Invalid option.")
