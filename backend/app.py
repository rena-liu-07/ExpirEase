from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# --- Database paths ---
USER_DB = "users.db"
FOOD_DB = os.path.abspath(os.path.join(os.path.dirname(__file__), "foodapp.db"))

# --- Init user database ---
def init_user_db():
    conn = sqlite3.connect(USER_DB)
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

init_user_db()

# ========================
# 🔑 AUTH ROUTES
# ========================

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        conn = sqlite3.connect(USER_DB)
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


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(USER_DB)
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


@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out"}), 200


# ========================
# 🥦 FOOD ROUTES
# ========================

def get_food_info(name):
    conn = sqlite3.connect(FOOD_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, date_added, expire_days FROM food WHERE LOWER(name) = LOWER(?)", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        name, category, date_added, expire_days = row
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        return {
            "name": name,
            "category": category,
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
    conn = sqlite3.connect(FOOD_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, date_added, expire_days FROM food")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for name, category, date_added, expire_days in rows:
        date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
        expire_date = date_added_dt + timedelta(days=expire_days)
        result.append({
            "name": name,
            "category": category,
            "expiration": expire_date.strftime("%Y-%m-%d")
        })
    return jsonify(result)


@app.route("/delete-ingredient", methods=["DELETE"])
def delete_ingredient():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "No name provided"}), 400
    conn = sqlite3.connect(FOOD_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


# ========================
# 🍳 RECIPE ROUTES
# ========================

@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    """Generate a recipe using available ingredients from the database."""
    try:
        # Import here to avoid circular imports
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        import recipe_maker
        
        data = request.get_json() or {}
        user_id = data.get('user_id')
        recipe_size = data.get('recipe_size', 'medium')
        dietary_restrictions = data.get('dietary_restrictions', '')
        cuisine_preference = data.get('cuisine_preference', '')
        prioritize_expiring = data.get('prioritize_expiring', True)
        
        if user_id:
            recipe = recipe_maker.make_recipe_for_user(
                user_id, recipe_size, dietary_restrictions, cuisine_preference, prioritize_expiring
            )
        else:
            recipe = recipe_maker.make_recipe_from_general_inventory(
                recipe_size, dietary_restrictions, cuisine_preference, prioritize_expiring
            )
        
        return jsonify({'recipe': recipe, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route("/expiring-ingredients", methods=["GET"])
def expiring_ingredients():
    """Get ingredients that are expiring soon."""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        import recipe_maker
        
        user_id = request.args.get('user_id', type=int)
        days_threshold = request.args.get('days_threshold', default=3, type=int)
        
        expiring_foods = recipe_maker.get_expiring_foods(user_id, days_threshold)
        
        result = []
        for name, days_left, extra_info in expiring_foods:
            result.append({
                'name': name,
                'days_until_expiry': days_left,
                'category_or_nutrition': extra_info
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}, 500)


# ========================
# 🚀 Run the unified server
# ========================

@app.route("/", methods=["GET"])
def home():
    return "✅ Unified Flask API running! Available: /signup, /login, /logout, /search, /all-ingredients"

if __name__ == "__main__":
    app.run(debug=True, port=5000)

