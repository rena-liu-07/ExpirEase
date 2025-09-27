from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

DB_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "foodapp.db"))

def get_food_info(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, date_added, expire_days, nutrition FROM food WHERE LOWER(name) = LOWER(?)", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        name, date_added, expire_days, nutrition = row
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        return {
            "name": name,
            "category": nutrition,  # Adjust if you have a separate category field
            "expiration": expire_date.strftime("%Y-%m-%d")
        }
    return None

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    result = get_food_info(query)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Not found"}), 404

@app.route("/all-ingredients", methods=["GET"])
def all_ingredients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, date_added, expire_days, nutrition FROM food")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for name, date_added, expire_days, nutrition in rows:
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        result.append({
            "name": name,
            "category": nutrition,
            "expiration": expire_date.strftime("%Y-%m-%d")
        })
    return jsonify(result)

@app.route("/delete-ingredient", methods=["DELETE"])
def delete_ingredient():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "No name provided"}), 400
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
