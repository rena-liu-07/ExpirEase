import requests
import json

try:
    response = requests.get('http://127.0.0.1:5000/all-ingredients')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Type: {type(data)}")
        print(f"Number of ingredients: {len(data) if isinstance(data, list) else 'Not a list'}")
        if isinstance(data, list) and len(data) > 0:
            print("Sample ingredients:")
            for i, item in enumerate(data[:3]):
                print(f"  {i+1}. {item}")
    else:
        print(f"Error response: {response.text}")
except Exception as e:
    print(f"Connection error: {e}")