import sqlite3
from datetime import datetime, timedelta
import os
import hashlib

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

# create/connect to database

# user_info.py
conn = sqlite3.connect("foodapp.db") 

# create user_food table
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password_hash TEXT,
    created_at TEXT
)
""")

# ====== DATABASE CONNECTION ======
def get_connection():
    return sqlite3.connect(DB_NAME)

# ====== PASSWORD HASHING ======
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ====== USER FUNCTIONS ======
def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    password_hash = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO user (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, created_at)
        )
        conn.commit()
        print(f"User {username} registered.")
    except sqlite3.IntegrityError:
        print(f"Username {username} already exists.")
    conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute(
        "SELECT id FROM user WHERE username=? AND password_hash=?",
        (username, password_hash)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        print(f"User {username} logged in.")
        return row[0]  # user_id
    else:
        print("Login failed.")
        return None

# ====== USER FOOD FUNCTIONS ======
def add_user_food(user_id, food_name, expire_days=None, nutrition=""):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    # get default expire_days from catalog if not provided
    if expire_days is None:
        cursor.execute("SELECT default_expire_days FROM food_catalog WHERE name=?", (food_name,))
        row = cursor.fetchone()
        expire_days = row[0] if row else 3
    # insert into food table
    cursor.execute(
        "INSERT INTO food (name, date_added, expire_days, nutrition) VALUES (?, ?, ?, ?)",
        (food_name, today, expire_days, nutrition)
    )
    food_id = cursor.lastrowid
    # insert into user_food
    cursor.execute(
        "INSERT INTO user_food (user_id, food_id, date_added, expire_days, nutrition) VALUES (?, ?, ?, ?, ?)",
        (user_id, food_id, today, expire_days, nutrition)
    )
    conn.commit()
    conn.close()
    print(f"Added {food_name} for user_id {user_id}.")

def check_user_food_status(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now()
    cursor.execute("""
    SELECT f.name, uf.date_added, uf.expire_days, uf.nutrition
    FROM user_food uf
    JOIN food f ON uf.food_id = f.id
    WHERE uf.user_id=?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for name, date_added, expire_days, nutrition in rows:
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        days_left = (expire_date - today).days
        status = "expired" if days_left < 0 else f"good, {days_left} days left"
        result.append((name, status, nutrition))
    return result

# ====== DEMO ======
if __name__ == "__main__":
    # test register and login
    register_user("demo", "demo@example.com", "123456")
    user_id = login_user("demo", "123456")
    if user_id:
        add_user_food(user_id, "apple")
        add_user_food(user_id, "banana", nutrition="calories:89, protein:1.1g")
        foods = check_user_food_status(user_id)
        print("\n--- User Food Status ---")
        for name, status, nutrition in foods:
            print(f"{name}: {status}, nutrition: {nutrition}")
