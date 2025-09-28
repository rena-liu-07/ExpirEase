from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "users.db"

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# 首页测试
@app.route("/", methods=["GET"])
def home():
    return "✅ Flask is running! Try /signup or /login"


# 注册
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return "This is the signup page. Please send POST request with username, email, password."

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({"user_id": user_id}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 400


# 登录
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return "This is the login page. Please send POST request with username, password."

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"user_id": row[0]}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        return "This is the logout page. Just send POST to logout."

    return jsonify({"message": "Logged out"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
