import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from datetime import datetime, timedelta
from shelf_life_api import estimate_expiration, get_expiry_from_stilltasty

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_image(image_path):
    # Open image and convert to bytes
    im = Image.open(image_path)
    # Send prompt and image to Gemini for analysis
    prompt = {"text": "Identify all food items in the image and, if present, extract the labeled expiration date for each. If no label is present, estimate the expiration date for fruits or non-labeled items based on today's date. For each item, respond in the format: Item: <item>\nExpiration: <date>. List each item on a new line."}
    response = model.generate_content(contents=[prompt, im])
    items = []
    # Parse Gemini response
    if response and response.candidates:
        text = response.candidates[0].content.parts[0].text
        current_item = None
        current_exp = None
        # Improved parsing logic to handle multiple items
        for line in text.splitlines():
            if 'item' in line.lower():
                if current_item:
                    # Save previous item before starting new
                    items.append({'item': current_item, 'expiration': current_exp})
                current_item = line.split(':', 1)[-1].strip()
                current_exp = None
            elif 'expiration' in line.lower():
                current_exp = line.split(':', 1)[-1].strip()
        # Add last item if present
        if current_item:
            items.append({'item': current_item, 'expiration': current_exp})
    # Estimate expiration for items missing it
    for entry in items:
        if not entry['expiration'] and entry['item']:
            #print(f"No labeled expiration found for {entry['item']}, estimating.")
            #entry['expiration'] = estimate_expiration(entry['item'])

            expiry_info = estimate_expiration(current_item)
            print(f"Estimated expiry for {current_item}: {expiry_info}")
    return items

def estimate_expiration(item):
    # Example logic: fruits last 5 days, candy 30 days, etc.
    today = datetime.today()
    item = item.lower()
    if 'banana' in item or 'grape' in item:
        return (today + timedelta(days=5)).strftime('%Y-%m-%d')
    elif 'candy' in item:
        return (today + timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        return (today + timedelta(days=7)).strftime('%Y-%m-%d')
    
if __name__ == '__main__':
    image_path = 'sample.jpg'  # Replace with your image file
    items = analyze_image(image_path)
    for entry in items:
        print(f"Item: {entry['item']}")
        print(f"Expiration: {entry['expiration']}")
