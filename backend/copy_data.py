import sqlite3
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

<<<<<<< HEAD
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ====== CREATE TABLES ======
=======
# ====== CREATE TABLES ======
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

>>>>>>> 0f2e8d1cd45c0e1d9a38e13fe7f3419b4a5997d5
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

<<<<<<< HEAD
# ====== RUN ONCE ======
if __name__ == "__main__":
    init_common_categories()
=======
def populate_example_foods():
    # 每个类别至少放一个示例
    example_foods = [
        ("Apple", 7, "Fruit"),
        ("Banana", 5, "Fruit"),
        ("Carrot", 10, "Vegetable"),
        ("Broccoli", 8, "Vegetable"),
        ("Chicken Breast", 5, "Meat"),
        ("Salmon", 4, "Seafood"),
        ("Milk", 7, "Dairy"),
        ("Cheese", 14, "Dairy"),
        ("Bread", 3, "Grain"),
        ("Rice", 180, "Grain"),
        ("Almonds", 365, "Nut"),
        ("Chocolate Bar", 180, "Snack"),
        ("Coke", 365, "Beverage"),
        ("Salt", 365, "Condiment"),
        ("Frozen Peas", 180, "Frozen Food"),
        ("Canned Corn", 365, "Canned Food"),
        ("Black Pepper", 365, "Spice"),
        ("Croissant", 3, "Pastry")
    ]
    for name, expire_days, category in example_foods:
        add_food(name, expire_days, category)

# ====== RUN ONCE ======
if __name__ == "__main__":
    init_common_categories()
    populate_example_foods()
    print("Database initialized and example foods added!")
>>>>>>> 0f2e8d1cd45c0e1d9a38e13fe7f3419b4a5997d5
