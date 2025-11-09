import requests

r = requests.get('http://localhost:5000/all-ingredients')
data = r.json()

print(f'Total ingredients: {len(data)}')

# Search for Apple
apple_foods = [f for f in data if 'apple' in f['name'].lower()]
print(f'\nApple-related foods: {len(apple_foods)}')
for f in apple_foods:
    print(f"  {f['name']} - {f['days_until_expiry']} days left - {f['category']}")

# Show last 5 items (most recently added)
print(f"\nLast 5 items:")
for f in data[-5:]:
    print(f"  {f['name'][:50]} - {f['days_until_expiry']} days left")
