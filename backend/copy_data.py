from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端跨域访问

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

# ====== DATABASE HELPERS ======
def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

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
    CREATE TABLE IF NOT EXISTS food_category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()

# ====== API ======
@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    data = request.get_json()
    name = data.get("name")
    category = data.get("category")
    expiration_date = data.get("expiration_date")

    if not all([name, category, expiration_date]):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    # 计算过期天数
    today = datetime.now().strftime("%Y-%m-%d")
    expire_days = (datetime.strptime(expiration_date, "%Y-%m-%d") - datetime.strptime(today, "%Y-%m-%d")).days

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO food (name, date_added, expire_days, category) VALUES (?, ?, ?, ?)",
        (name, today, expire_days, category)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/my_foods", methods=["GET"])
def my_foods():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, date_added, expire_days, category FROM food")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for name, date_added, expire_days, category in rows:
        expire_date = datetime.strptime(date_added, "%Y-%m-%d") + timedelta(days=expire_days)
        result.append({
            "name": name,
            "category": category,
            "expiration_date": expire_date.strftime("%Y-%m-%d")
        })

    return jsonify(result)

# ====== RUN ======
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)

