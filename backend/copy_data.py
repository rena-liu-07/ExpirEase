import sqlite3
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ====== CREATE TABLES ======
cursor.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date_added TEXT,
    expire_days INTEGER,
    category TEXT
)               
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS food_catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    default_expire_days INTEGER
)
""") 

cursor.execute("""
CREATE TABLE IF NOT EXISTS food_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

conn.commit()
conn.close()

# ====== FUNCTIONS ======
def add_to_catalog(name, default_expire_days):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO food_catalog (name, default_expire_days) VALUES (?, ?)",
        (name, default_expire_days)
    )
    conn.commit()
    conn.close()

def add_food(name, expire_days, category):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO food (name, date_added, expire_days, category) VALUES (?, ?, ?, ?)",
        (name, today, expire_days, category)
    )
    conn.commit()
    conn.close()

def add_category(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO food_category (name) VALUES (?)",
        (name,)
    )
    # close the connection
    conn.commit()
    conn.close()

def check_food_status():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = datetime.now()
    cursor.execute("SELECT name, date_added, expire_days, category FROM food")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for name, date_added, expire_days, category in rows:
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        days_left = (expire_date - today).days
        status = "expired" if days_left < 0 else f"{days_left} days left"
        result.append((name, status, category))
    return result

def init_common_categories():
    common_categories = [
        "Fruit",
        "Vegetable",
        "Meat",
        "Seafood",
        "Dairy",
        "Grain",
        "Nut",
        "Snack",
        "Beverage",
        "Condiment",
        "Frozen Food",
        "Canned Food",
        "Spice",
        "Pastry"
    ]
    for cat in common_categories:
        add_category(cat)

# ====== RUN ONCE ======
if __name__ == "__main__":
    init_common_categories()