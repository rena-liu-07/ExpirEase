from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
import os
import sys

# Add backend directory to Python path for imports
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import backend modules
from backend import scanner, food_data

app = Flask(__name__)
CORS(app)

# Authentication database setup
AUTH_DB_NAME = "users.db"

def init_auth_db():
    conn = sqlite3.connect(AUTH_DB_NAME)
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

init_auth_db()

# Authentication endpoints
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        conn = sqlite3.connect(AUTH_DB_NAME)
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    try:
        conn = sqlite3.connect(AUTH_DB_NAME)
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out"}), 200

@app.route("/photo_scanner", methods=['POST'])
def photo_scanner():
    """Photo scanning endpoint for food recognition"""
    print("=== PHOTO_SCANNER ENDPOINT HIT ===")
    print(f"Request method: {request.method}")
    print(f"Request files: {list(request.files.keys())}")
    
    try:
        # Check for 'image' (singular) or 'images' (plural)
        image_files = []
        if 'image' in request.files:
            image_files = [request.files['image']]
        elif 'images' in request.files:
            image_files = request.files.getlist('images')
        else:
            print("No image/images field found in request")
            return jsonify({'error': 'No images uploaded', 'received_keys': list(request.files.keys())}), 400
        
        print(f"Found {len(image_files)} image files")
        
        # Process each image
        results = []
        for i, image_file in enumerate(image_files):
            print(f"Processing image {i+1}: {image_file.filename}")
            try:
                # Save the uploaded file temporarily
                temp_path = f"temp_upload_{i}.jpg"
                image_file.save(temp_path)
                
                # Analyze the image and add to database
                items = scanner.analyze_image(temp_path)
                results.append(items)
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                print(f"Error processing image {i+1}: {str(e)}")
                import traceback
                traceback.print_exc()
                results.append([{'item': 'Error', 'error': str(e)}])
        
        print("Analysis complete, returning results")
        return jsonify({"results": results, "success": True}), 200
        
    except Exception as e:
        print(f"Error in photo_scanner: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/')
def home():
    """Root endpoint to verify server is running"""
    return jsonify({
        "message": "ExpirEase API Server is running!",
        "endpoints": {
            "auth": ["/signup", "/login", "/logout"],
            "recipes": ["/generate-recipe"],
            "ingredients": ["/all-ingredients", "/expiring-ingredients", "/add_ingredient", "/delete-ingredient"],
            "search": ["/search?q=<query>"],
            "photo": ["/photo_scanner (POST)"]
        }
    }), 200

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe_endpoint():
    """Recipe generation endpoint"""
    try:
        import recipe_maker
        
        data = request.get_json()
        recipe_size = data.get('recipe_size', 'medium')
        dietary_restrictions = data.get('dietary_restrictions', '')
        cuisine_preference = data.get('cuisine_preference', '')
        prioritize_expiring = data.get('prioritize_expiring', True)
        
        recipe = recipe_maker.make_recipe_from_general_inventory(
            recipe_size, dietary_restrictions, cuisine_preference, prioritize_expiring
        )
        return jsonify({'recipe': recipe, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/all-ingredients', methods=['GET'])
def all_ingredients():
    """Get all ingredients from the database"""
    try:
        from recipe_maker import get_user_foods
        from datetime import datetime
        ingredients_tuples = get_user_foods(None)  # Get all ingredients
        
        print(f"DEBUG: Total ingredients retrieved from database: {len(ingredients_tuples)}")
        
        # Convert tuples to JSON objects
        ingredients = []
        for name, days_left, category in ingredients_tuples:
            ingredients.append({
                'id': len(ingredients) + 1,
                'name': name,
                'category': category,
                'expiration': (datetime.now() + timedelta(days=days_left)).strftime('%Y-%m-%d'),
                'days_until_expiry': days_left
            })
        
        print(f"DEBUG: Returning {len(ingredients)} ingredients to frontend")
        return jsonify(ingredients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/expiring-ingredients', methods=['GET'])  
def expiring_ingredients():
    """Get ingredients that are expiring soon"""
    try:
        from recipe_maker import get_user_foods
        from datetime import datetime, timedelta
        ingredients_tuples = get_user_foods(None, include_expiring_soon=True)
        
        # Convert tuples to JSON objects
        ingredients = []
        for name, days_left, category in ingredients_tuples:
            ingredients.append({
                'id': len(ingredients) + 1,
                'name': name,
                'category': category,
                'expiration': (datetime.now() + timedelta(days=days_left)).strftime('%Y-%m-%d'),
                'days_until_expiry': days_left
            })
        return jsonify(ingredients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['GET'])
def search_ingredient():
    """Search for a specific ingredient"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        from recipe_maker import get_user_foods
        ingredients_tuples = get_user_foods(None)
        # Simple search - find ingredient by name
        for name, days_left, category in ingredients_tuples:
            if query.lower() in name.lower():
                return jsonify({
                    'name': name,
                    'category': category,
                    'expiration': (datetime.now() + timedelta(days=days_left)).strftime('%Y-%m-%d'),
                    'days_until_expiry': days_left
                })
        return jsonify({'error': 'Ingredient not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-ingredient', methods=['DELETE'])
def delete_ingredient():
    """Delete an ingredient by name"""
    try:
        print("=== DELETE_INGREDIENT ENDPOINT HIT ===")
        name = request.args.get('name', '')
        print(f"Attempting to delete ingredient: {name}")
        
        if not name:
            print("Error: No ingredient name provided")
            return jsonify({'error': 'No ingredient name provided'}), 400
        
        from backend.food_data import delete_food
        delete_food(name)
        print(f"Successfully deleted ingredient: {name}")
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in delete_ingredient: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500



# Add ingredient endpoint
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    try:
        print("=== ADD_INGREDIENT ENDPOINT HIT ===")
        from backend.food_data import add_food
        
        data = request.get_json()
        print(f"Received data: {data}")
        
        name = data.get('name')
        category = data.get('category')
        expiration_date = data.get('expiration_date')
        
        print(f"Name: {name}, Category: {category}, Expiration: {expiration_date}")
        
        today = datetime.now()
        expire_days = None
        if expiration_date:
            expire_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            expire_days = (expire_date - today).days
            if expire_days < 0:
                expire_days = 0
        else:
            expire_days = 7
        
        print(f"Calculated expire_days: {expire_days}")
        add_food(name, expire_days, category)
        print(f"Successfully added {name} to database")
        
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Error in add_ingredient: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
