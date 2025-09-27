from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)
DB_NAME = os.path.join(os.path.dirname(__file__), "foodapp.db")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute("SELECT id FROM user WHERE username=? AND password=?", (username, password_hash))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"user_id": row[0]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    password_hash = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO user (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, created_at)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({"user_id": user_id})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Username already exists"}), 409

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")