from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

# ==== 数据库连接函数 ====
def get_connection():
    return sqlite3.connect(DB_NAME)

# ==== 初始化用户食物表 ====
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        food_name TEXT,
        category TEXT,
        date_added TEXT
    )
    """)
    conn.commit()
    conn.close()

# ==== 添加用户食物 ====
def add_user_food(user_id, food_name, category):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO user_food (user_id, food_name, category, date_added) VALUES (?, ?, ?, ?)",
        (user_id, food_name, category, today)
    )
    conn.commit()
    conn.close()

# ==== Flask 路由 ====
@app.route("/add-food", methods=["POST"])
def route_add_food():
    data = request.get_json()
    user_id = data.get("user_id")
    food_name = data.get("food_name")
    category = data.get("category")

    # 检查字段是否存在
    if not (user_id and food_name and category):
        return jsonify({"error": "Missing fields"}), 400

    add_user_food(user_id, food_name, category)
    return jsonify({"success": True, "food_name": food_name, "category": category})

# ==== 获取用户食物（可选调试用） ====
@app.route("/my-foods", methods=["GET"])
def route_get_food():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT food_name, category, date_added FROM user_food WHERE user_id=?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    result = [{"food_name": r[0], "category": r[1], "date_added": r[2]} for r in rows]
    return jsonify(result)

# ==== 启动 ====
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

