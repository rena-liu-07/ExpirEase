import requests
import json
from datetime import datetime, timedelta

# Test data
test_food = {
    "name": "Test Banana",
    "category": "Fruit",
    "expiration_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
}

print("Testing /add-ingredient endpoint...")
print(f"Sending: {json.dumps(test_food, indent=2)}")

# Test with hyphen (what backend expects)
try:
    response = requests.post('http://localhost:5000/add-ingredient', json=test_food)
    print(f"\n/add-ingredient (hyphen) - Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"/add-ingredient (hyphen) - ERROR: {e}")

# Test with underscore (what frontend sends)
try:
    response = requests.post('http://localhost:5000/add_ingredient', json=test_food)
    print(f"\n/add_ingredient (underscore) - Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"/add_ingredient (underscore) - ERROR: {e}")
