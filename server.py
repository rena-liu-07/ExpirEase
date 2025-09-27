from flask import Flask, request, jsonify
import photo_scanner
import recipe_maker
import shelf_life_api

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
