import requests
import json
import os

# Test the photo_scanner endpoint with absolute path
test_data = {
    "paths": [os.path.abspath("pictures/test_apple.jpg")]
}

print("Testing /photo_scanner endpoint...")
print(f"Sending: {json.dumps(test_data, indent=2)}")

try:
    response = requests.post('http://localhost:5000/photo_scanner', json=test_data)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"ERROR: {e}")
