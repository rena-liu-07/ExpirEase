import sqlite3
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

# ====== DATABASE INITIALIZATION ======
conn = get_connection()
cursor = conn.cursor()

# User's personal food table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_food (
    user_id INTEGER,
    food_name TEXT,
    date_added TEXT,
    expire_days INTEGER,
    nutrition TEXT
)
""")

# User's favorites table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_favorites (
    user_id INTEGER,
    item_name TEXT,
    date_added TEXT
)
""")

conn.commit()
conn.close()

# ====== USER FOOD FUNCTIONS ======
def add_user_food(user_id, food_name, expire_days=None, nutrition=""):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    if expire_days is None:
        expire_days = 3  # default expire days
    cursor.execute(
        "INSERT INTO user_food (user_id, food_name, date_added, expire_days, nutrition) VALUES (?, ?, ?, ?, ?)",
        (user_id, food_name, today, expire_days, nutrition)
    )
    conn.commit()
    conn.close()
    print(f"Added '{food_name}' for user_id {user_id}.")

def check_user_food_status(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now()
    cursor.execute(
        "SELECT food_name, date_added, expire_days, nutrition FROM user_food WHERE user_id=?",
        (user_id,)
    )
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

# ====== USER FAVORITES FUNCTIONS ======
def add_to_favorites(user_id, item_name):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO user_favorites (user_id, item_name, date_added) VALUES (?, ?, ?)",
        (user_id, item_name, today)
    )
    conn.commit()
    conn.close()
    print(f"Added '{item_name}' to favorites for user_id {user_id}.")

def list_favorites(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_name, date_added FROM user_favorites WHERE user_id=?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("No favorites yet.")
        return []
    print("\n--- Favorites ---")
    for name, date_added in rows:
        print(f"{name}, added on {date_added}")
    return rows

# ====== DEMO CLI ======
if __name__ == "__main__":
    user_id = int(input("Enter user_id (from login system): ").strip())

    while True:
        print("\n--- User Food Menu ---")
        print("1. Add Food")
        print("2. Check Food Status")
        print("3. Add to Favorites")
        print("4. List Favorites")
        print("5. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            food_name = input("Food name: ").strip()
            nutrition = input("Nutrition info (optional): ").strip()
            add_user_food(user_id, food_name, nutrition=nutrition)
        elif choice == "2":
            foods = check_user_food_status(user_id)
            print("\n--- User Food Status ---")
            for name, status, nutrition in foods:
                print(f"{name}: {status}, nutrition: {nutrition}")
        elif choice == "3":
            item_name = input("Item to add to favorites: ").strip()
            add_to_favorites(user_id, item_name)
        elif choice == "4":
            list_favorites(user_id)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option.")

