"""import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from datetime import datetime
from shelf_life_api import estimate_expiration
from food_data import add_food, add_to_catalog

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_image(image_path):
    # Open image and convert to bytes
    im = Image.open(image_path)
    today_str = datetime.today().strftime('%Y-%m-%d')
    # Send prompt and image to Gemini for analysis
    prompt = {
        "text": (
            f"Today's date is {today_str}. "
            "Identify all food items in the image and, if present, extract the labeled expiration date for each and determine how many days that is from today's date. "
            "If no label is present, estimate the expiration date for fruits or non-labeled items with as much detail as possible. "
            "For each item, respond in the format: Item: <item>\nExpiration: <days>. List each item on a new line. "
            "Each container can be counted as one item."
        )
    }
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
            expiry_info = estimate_expiration(entry['item'])
            entry['expiration'] = expiry_info
            print(f"Estimated expiry for {entry['item']}: {expiry_info}")
     
    return items


if __name__ == '__main__':
    import sys
    image_paths = sys.argv[1:] if len(sys.argv) > 1 else ['pictures/sample.jpg']
    all_items = []
    for image_path in image_paths:
        print(f"Processing: {image_path}")
        items = analyze_image(image_path)
        for entry in items:
            print(f"Item: {entry['item']}")
            print(f"Expiration: {entry['expiration']}")
        all_items.extend(items)"""

import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from datetime import datetime
from shelf_life_api import estimate_expiration
from food_data import add_food, check_food_status

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_image(image_path):
    # Open image and convert to bytes
    im = Image.open(image_path)
    today_str = datetime.today().strftime('%Y-%m-%d')
    # Send prompt and image to Gemini for analysis
    prompt = {
        "text": (
            f"Today's date is {today_str}. "
            "Identify all food items in the image and, if present, extract the labeled expiration date for each and determine how many days that is from today's date return only the number of days until the product expires. "
            "If no label is present, estimate the number of days for the non-labeled items to expire with as much detail as possible. "
            "For each item, respond in the format: Item: <item>\nExpiration: <day>. List each item on a new line. "
            "Each container can be counted as one item."
        )
    }
    response = model.generate_content(contents=[prompt, im])
    items = []
    # Parse Gemini response
    if response and response.candidates:
        text = response.candidates[0].content.parts[0].text
        print("Gemini raw response:\n", text)  # Debugging line
        current_item = None
        current_exp = None
        # Improved parsing logic to handle multiple items
        for line in text.splitlines():
            if 'item' in line.lower():
                if current_item:
                    items.append({'item': current_item, 'expiration': current_exp})
                current_item = line.split(':', 1)[-1].strip()
                current_exp = None
            elif 'expiration' in line.lower():
                current_exp = line.split(':', 1)[-1].strip()
        if current_item:
            items.append({'item': current_item, 'expiration': current_exp})
    # Estimate expiration for items missing it
    for entry in items:
        if not entry['expiration'] and entry['item']:
            expiry_info = estimate_expiration(entry['item'])
            entry['expiration'] = expiry_info
            print(f"Estimated expiry for {entry['item']}: {expiry_info}")

    # Calculate days left and add to database
    for entry in items:
        days_left = None
        if entry.get('expiration'):
            try:
                expire_date = datetime.strptime(entry['expiration'], "%Y-%m-%d")
                days_left = (expire_date - datetime.today()).days
                if days_left < 0:
                    days_left = 0
            except Exception:
                # If expiration is not a date, fallback to 7 days
                days_left = 7
        else:
            days_left = 7
        print(f"Item: {entry['item']}")
        print(f"Days before expiration: {days_left}")
        add_food(entry['item'], days_left)

    return items

if __name__ == '__main__':
    import sys
    image_paths = sys.argv[1:] if len(sys.argv) > 1 else ["pictures/cookie_test.jpg"]
    all_items = []
    for image_path in image_paths:
        print(f"Processing: {image_path}")
        items = analyze_image(image_path)
        all_items.extend(items)
    
    status_list = check_food_status()
    print("\nFood Status:")
    for name, status in status_list:
        print(f"{name}: {status}")
        