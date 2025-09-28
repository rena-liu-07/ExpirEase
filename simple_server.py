import sys
import os
sys.path.append(os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is working!', 'status': 'OK'})

@app.route('/all-ingredients', methods=['GET'])
def all_ingredients():
    """Get all ingredients from the database"""
    try:
        # Test with direct database access
        import sqlite3
        from datetime import datetime, timedelta
        
        conn = sqlite3.connect('foodapp.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, category, expire_days FROM food LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        
        ingredients = []
        for i, (name, category, expire_days) in enumerate(rows):
            ingredients.append({
                'id': i + 1,
                'name': name,
                'category': category,
                'expiration': (datetime.now() + timedelta(days=expire_days)).strftime('%Y-%m-%d'),
                'days_until_expiry': expire_days
            })
        
        return jsonify(ingredients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting simplified Flask server on port 5000...")
    app.run(host='127.0.0.1', port=5000, debug=False)