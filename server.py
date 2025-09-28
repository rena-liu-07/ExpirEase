from flask import Flask, request, jsonify
import photo_scanner
import recipe_maker
import shelf_life_api
from food_data import add_food

app = Flask(__name__)

@app.route('/photo_scanner', methods=['POST'])
def photo_scanner_endpoint():
    image_paths = request.json.get('paths', [])
    # photo_scanner.run should return a list of items for each image
    results = photo_scanner.run(image_paths)
    return jsonify({'results': results})

@app.route('/recipe_maker', methods=['POST'])
def recipe_maker_endpoint():
    image_paths = request.json.get('paths', [])
    size = request.json.get('size', (100, 100))
    results = [recipe_maker.run(path, size) for path in image_paths]
    return jsonify({'results': results})



# Add ingredient endpoint
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')
    expiration_date = data.get('expiration_date')
    # Calculate expire_days from expiration_date
    from datetime import datetime
    try:
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
    app.run(host='0.0.0.0', port=8080)
