from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import scanner

app = Flask(__name__)
CORS(app)

@app.route("/test", methods=["GET"])
def test():
    return "OK"

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

@app.route("/test", methods=['GET', 'POST'])
def test_endpoint():
    print("=== TEST ENDPOINT HIT - UPDATED VERSION ===")
    return jsonify({"message": "Flask server is working - UPDATED VERSION", "method": request.method, "timestamp": "2025-09-28"})

@app.route("/photo_scanner", methods=['POST'])
def photo_scanner():
    print("=== PHOTO_SCANNER ENDPOINT HIT ===")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request content type: {request.content_type}")
    
    try:
        print("POST request received to /photo_scanner")
        print("Files in request:", list(request.files.keys()))
        
        if 'images' not in request.files:
            print("No 'images' field found in request.files")
            return jsonify({'error': 'No images uploaded'}), 400
        
        image_files = request.files.getlist('images')
        print(f"Found {len(image_files)} image files")
        
        # Use the analyze_image function from scanner.py
        results = []
        for i, image_file in enumerate(image_files):
            print(f"Processing image {i+1}: {image_file.filename}")
            try:
                result = scanner.analyze_image(image_file)
                results.append(result)
            except Exception as e:
                print(f"Error processing image {i+1}: {str(e)}")
                # Return a dummy result for testing
                results.append([{'item': 'UPDATED SERVER - Test Item', 'expiration': '7 days'}])
        
        print("Analysis complete, returning results")
        return jsonify({"results": results})
    except Exception as e:
        print(f"Error in photo_scanner: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
