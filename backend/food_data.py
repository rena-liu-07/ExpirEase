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
    nutrition TEXT
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

# ====== FUNCTIONS ======
def add_to_catalog(name, default_expire_days):
    cursor.execute(
        "INSERT OR IGNORE INTO food_catalog (name, default_expire_days) VALUES (?, ?)",
        (name, default_expire_days)
    )

def add_food(name, expire_days, nutrition=""):
    # Create a new connection for this thread to avoid threading issues
    local_conn = sqlite3.connect(DB_NAME)
    local_cursor = local_conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    local_cursor.execute(
        "INSERT INTO food (name, date_added, expire_days, nutrition) VALUES (?, ?, ?, ?)",
        (name, today, expire_days, nutrition)
    )
    local_conn.commit()
    local_conn.close()

def add_category(name):
    cursor.execute(
        "INSERT OR IGNORE INTO food_category (name) VALUES (?)",
        (name,)
    )

def check_food_status():
    today = datetime.now()
    cursor.execute("SELECT name, date_added, expire_days, nutrition FROM food")
    rows = cursor.fetchall()
    result = []
    for name, date_added, expire_days, nutrition in rows:
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        days_left = (expire_date - today).days
        status = "expired" if days_left < 0 else f"good, {days_left} days left"
        result.append((name, status, nutrition))
    return result

# ====== CLEAR OLD DATA ======
cursor.execute("DELETE FROM food_catalog")
cursor.execute("DELETE FROM food")
cursor.execute("DELETE FROM food_category")
conn.commit()

# ====== INSERT FOOD CATALOG ======
big_catalog = [
    ("apple",5),("banana",3),("pear",4),("orange",5),("grape",7),("mango",6),
    ("kiwi",5),("strawberry",3),("blueberry",5),("watermelon",7),
    ("carrot",7),("lettuce",4),("spinach",3),("tomato",5),("potato",10),
    ("onion",15),("garlic",30),("cabbage",5),("broccoli",4),("cucumber",5),
    ("bell pepper",5),("mushroom",4),("zucchini",4),
    ("chicken",3),("beef",5),("pork",5),("lamb",4),("duck",3),
    ("fish",2),("shrimp",2),("crab",2),("salmon",2),("tuna",2),
    ("milk",7),("cheese",15),("yogurt",10),("butter",30),("cream",7),
    ("egg",10),
    ("tofu",5),("soybean",180),("lentil",180),("chickpea",180),
    ("rice",180),("pasta",180),("bread",7),("oats",180),("quinoa",180),
    ("olive oil",180),("vegetable oil",180),("vinegar",365),("salt",365),("sugar",365),
    ("chocolate",180),("biscuits",90),("nuts",180),("popcorn",180)
]

for name, days in big_catalog:
    add_to_catalog(name, days)

# ====== INSERT SAMPLE FOOD ======
sample_food = [
    ("apple",5,"calories:52, protein:0.3g"),
    ("banana",3,"calories:89, protein:1.1g"),
    ("milk",7,"calories:42, protein:3.4g"),
    ("cheese",15,"calories:402, protein:25g"),
    ("chicken",3,"calories:239, protein:27g"),
    ("beef",5,"calories:250, protein:26g"),
    ("egg",10,"calories:155, protein:13g"),
    ("carrot",7,"calories:41, protein:0.9g"),
    ("shrimp",2,"calories:99, protein:24g"),
    ("tofu",5,"calories:76, protein:8g"),
    ("rice",180,"calories:130, protein:2.7g"),
    ("bread",7,"calories:265, protein:9g")
]

for name, days, nutrition in sample_food:
    add_food(name, days, nutrition)

# ====== INSERT FOOD CATEGORIES ======
common_categories = [
    "Fruit", "Vegetable", "Meat", "Dairy", "Seafood",
    "Legume", "Grain", "Nut", "Oil", "Snack"
]

for category in common_categories:
    add_category(category)

conn.commit()

# ====== PRINT FOOD STATUS ======
status_list = check_food_status()
print("\n--- Food Status ---")
for name, status, nutrition in status_list:
    print(f"{name}: {status}, nutrition: {nutrition}")

conn.close()
