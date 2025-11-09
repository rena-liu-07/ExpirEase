import requests

# Test sending image file (like the frontend does)
image_path = r"C:\Users\ezhan\OneDrive\ExpirEase\ExpirEase-4\pictures\test_apple.jpg"

print("Testing /photo_scanner endpoint with file upload (like mobile app)...")
print(f"Image: {image_path}")

try:
    with open(image_path, 'rb') as f:
        files = {'image': ('test_apple.jpg', f, 'image/jpeg')}
        response = requests.post('http://localhost:5000/photo_scanner', files=files)
    
    print(f"\nStatus: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Count: {data.get('count')}")
    
    if data.get('results'):
        print(f"\nDetected items (results format):")
        for item in data['results'][0]:
            print(f"  - {item['item']} ({item['category']}) - expires: {item['expiration']}")
    
    if data.get('detected_items'):
        print(f"\nDetected items (detected_items format):")
        for item in data['detected_items']:
            print(f"  - {item['item']} ({item['category']}) - expires: {item['expiration']}")
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
