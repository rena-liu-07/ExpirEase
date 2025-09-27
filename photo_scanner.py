import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from datetime import datetime
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
    today_str = datetime.today().strftime('%Y-%m-%d')
    # Send prompt and image to Gemini for analysis
    prompt = {
        "text": (
            f"Today's date is {today_str}. "
            "Identify all food items in the image and, if present, extract the labeled expiration date for each. "
            "If no label is present, estimate the expiration date for fruits or non-labeled items based on today's date and with as much detail as possible. "
            "For each item, respond in the format: Item: <item>\nExpiration: <date>. List each item on a new line. "
            "Each container can be counted as one item. When estimating, use today's date as the reference."
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
    image_paths = sys.argv[1:]

    if not image_paths:
        print("No image paths provided.")
        sys.exit(1)

    all_items = []
    for image_path in image_paths:
        print(f"Processing: {image_path}")
        items = analyze_image(image_path)
        for entry in items:
            print(f"Item: {entry['item']}")
            print(f"Expiration: {entry['expiration']}")
        all_items.extend(items)