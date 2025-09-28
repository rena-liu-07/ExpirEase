import os
from PIL import Image
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
from shelf_life_api import estimate_expiration
from food_data import add_food, check_food_status

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Gemini client
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None
    print("Warning: No GEMINI_API_KEY found. Image analysis will not work.")

def analyze_image(image_path):
    print("analyze_image function called")
    print(f"model is None: {model is None}")
    print(f"GEMINI_API_KEY exists: {GEMINI_API_KEY is not None}")
    
    if model is None:
        print("No Gemini model available, returning dummy data")
        return [{'item': 'Dummy Item', 'expiration': '7'}]
    
    # Accept file-like object or file path
    if hasattr(image_path, 'read'):
        im = Image.open(image_path)
        print("Opened image from file-like object")
    else:
        im = Image.open(str(image_path))
        print(f"Opened image from path: {image_path}")
        
    today_str = datetime.today().strftime('%Y-%m-%d')
    print(f"Today's date: {today_str}")
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
    print("About to call Gemini API...")
    try:
        import time
        start_time = time.time()
        response = model.generate_content(contents=[prompt, im])
        end_time = time.time()
        print(f"Gemini response received in {end_time - start_time:.2f} seconds")
        print(f"Response object: {response}")
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        import traceback
        traceback.print_exc()
        return [{'item': 'API Error Item', 'expiration': '7'}]
    
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

def scanner(image_paths):
    all_items = []
    for image_path in image_paths:
        print(f"Processing: {image_path}")
        items = analyze_image(image_path)
        all_items.extend(items)
    return all_items

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(len(sys.argv))
        image_paths = sys.argv[1:] 
        all_items = []
        for image_path in image_paths:
            print(f"Processing: {image_path}")
            items = analyze_image(image_path)
            all_items.extend(items)
    else:
        print("No images provided.")
        """image_paths = ["pictures/test_apple.jpg"]
        print("No images provided. Using default test image.")
        all_items = []
        for image_path in image_paths:
            print(f"Processing: {image_path}")
            items = analyze_image(image_path)
            all_items.extend(items)"""
    print("dsagmklds")
    status_list = check_food_status()
    print("\nFood Status:")
    for name, status in status_list:
        print(f"{name}: {status}")
        