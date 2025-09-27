import sqlite3
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

def add_to_catalog(name, default_expire_days):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO food_catalog (name, default_expire_days) VALUES (?, ?)",
            (name, default_expire_days)
        )
        conn.commit()
        conn.close()
        print(f"Catalog: {name}, expire {default_expire_days} days")
    except sqlite3.IntegrityError:
        pass

def add_food(name, expire_days):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO food (name, date_added, expire_days) VALUES (?, ?, ?)",
        (name, today, expire_days)
    )
    conn.commit()
    conn.close()
    print(f"Food added: {name}, expires in {expire_days} days")

def check_food_status():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = datetime.now()
    cursor.execute("SELECT name, date_added, expire_days FROM food")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for name, date_added, expire_days in rows:
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        days_left = (expire_date - today).days
        status = "expired" if days_left < 0 else f"good, {days_left} days left"
        result.append([name, status])
    return result