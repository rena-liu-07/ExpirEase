from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

# ====== DATABASE HELPERS ======
def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        food_name TEXT,
        category TEXT,
        date_added TEXT,
        expire_days INTEGER,
        nutrition TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        date_added TEXT
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

def init_common_categories():
    categories = [
        "Fruit", "Vegetable", "Meat", "Seafood", "Dairy",
        "Grain", "Nut", "Snack", "Beverage", "Condiment",
        "Frozen Food", "Canned Food", "Spice", "Pastry"
    ]
    conn = get_connection()
    cursor = conn.cursor()
    for cat in categories:
        cursor.execute("INSERT OR IGNORE INTO food_category (name) VALUES (?)", (cat,))
    conn.commit()
    conn.close()

# ====== USER FOOD FUNCTIONS ======
def add_user_food(user_id, food_name, category, expire_days=None, nutrition=""):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    if expire_days is None:
        expire_days = 3
    cursor.execute(
        "INSERT INTO user_food (user_id, food_name, category, date_added, expire_days, nutrition) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, food_name, category, today, expire_days, nutrition)
    )
    conn.commit()
    conn.close()

def get_user_food(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT food_name, category, date_added, expire_days, nutrition FROM user_food WHERE user_id=?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    result = []
    for name, category, date_added, expire_days, nutrition in rows:
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        result.append({
            "name": name,
            "category": category,
            "nutrition": nutrition,
            "expiration": expire_date.strftime("%Y-%m-%d")
        })
    return result

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

def list_favorites(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_name, date_added FROM user_favorites WHERE user_id=?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    result = []
    for name, date_added in rows:
        result.append({"name": name, "date_added": date_added})
    return result

# ====== FLASK ROUTES ======
@app.route("/add-food", methods=["POST"])
def route_add_food():
    data = request.get_json()
    user_id = data.get("user_id")
    food_name = data.get("food_name")
    category = data.get("category")
    expire_days = data.get("expire_days", 3)
    nutrition = data.get("nutrition", "")

    if not (user_id and food_name and category):
        return jsonify({"error": "Missing fields"}), 400


    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM food_category WHERE name=?", (category,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Invalid category"}), 400

    add_user_food(user_id, food_name, category, expire_days, nutrition)
    return jsonify({"success": True})

@app.route("/my-foods", methods=["GET"])
def route_get_food():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    foods = get_user_food(int(user_id))
    return jsonify(foods)

@app.route("/add-favorite", methods=["POST"])
def route_add_favorite():
    data = request.get_json()
    user_id = data.get("user_id")
    item_name = data.get("item_name")
    if not (user_id and item_name):
        return jsonify({"error": "Missing fields"}), 400
    add_to_favorites(user_id, item_name)
    return jsonify({"success": True})

@app.route("/my-favorites", methods=["GET"])
def route_list_favorites():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    favs = list_favorites(int(user_id))
    return jsonify(favs)

# ====== RUN ======
if __name__ == "__main__":
    init_db()
    init_common_categories()
    print("Database initialized with common categories.")
    app.run(debug=True)
