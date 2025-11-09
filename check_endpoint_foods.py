import requests

r = requests.get('http://localhost:5000/all-ingredients')
data = r.json()

print(f'Total ingredients from endpoint: {len(data)}')

test_foods = [f for f in data if 'Test' in f['name']]
print(f'Test foods found: {len(test_foods)}')

for f in test_foods:
    print(f"  {f['name']} - {f['days_until_expiry']} days left - category: {f['category']}")

if len(data) > 0:
    print(f"\nFirst 3 foods:")
    for f in data[:3]:
        print(f"  {f['name']} - {f['days_until_expiry']} days left")
