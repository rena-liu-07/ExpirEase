from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

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
    name = request.args.get('name', '')
    if not name:
        return jsonify({'error': 'No ingredient name provided'}), 400
    
    try:
        from food_data import delete_food
        delete_food(name)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Add ingredient endpoint
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    try:
        from food_data import add_food
        
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        expiration_date = data.get('expiration_date')
        
        today = datetime.now()
        expire_days = None
        if expiration_date:
            expire_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            expire_days = (expire_date - today).days
            if expire_days < 0:
                expire_days = 0
        else:
            expire_days = 7
        add_food(name, expire_days, category)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting Flask server on port 5000...")
    app.run(host='127.0.0.1', port=5000, debug=False)
