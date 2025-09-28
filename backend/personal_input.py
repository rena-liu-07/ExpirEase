from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

# ====== DATABASE HELPERS ======
def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 用户食材表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        food_name TEXT,
        category TEXT,
        date_added TEXT,
        expire_days INTEGER
    )
    """)

    # 食材分类表（可固定）
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

# ====== ROUTES ======
@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    data = request.get_json()
    user_id = data.get("user_id")
    name = data.get("name")
    category = data.get("category")
    exp_date = data.get("expiration_date")

    if not all([user_id, name, category, exp_date]):
        return jsonify({"error": "Missing fields"}), 400

    # 检查类别是否存在
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM food_category WHERE name=?", (category,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Invalid category"}), 400

    # 计算 expire_days
    today_str = datetime.now().strftime("%Y-%m-%d")
    expire_days = (datetime.strptime(exp_date, "%Y-%m-%d") - datetime.strptime(today_str, "%Y-%m-%d")).days

    cursor.execute(
        "INSERT INTO user_food (user_id, food_name, category, date_added, expire_days) VALUES (?, ?, ?, ?, ?)",
        (user_id, name, category, today_str, expire_days)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/my_foods", methods=["GET"])
def my_foods():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT food_name, category, date_added, expire_days FROM user_food WHERE user_id=?", 
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    result = []
    for name, category, date_added, expire_days in rows:
        expire_date = (datetime.strptime(date_added, "%Y-%m-%d") + timedelta(days=expire_days)).strftime("%Y-%m-%d")
        result.append({
            "name": name,
            "category": category,
            "expiration_date": expire_date
        })
    return jsonify(result)

# ====== RUN ======
if __name__ == "__main__":
    init_db()
    init_common_categories()
    print("Database initialized with common categories.")
    app.run(host="0.0.0.0", port=8080, debug=True)



