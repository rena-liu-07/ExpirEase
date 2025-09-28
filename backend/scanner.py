import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from datetime import datetime, timedelta
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
    # Open image and convert to bytes
    im = Image.open(image_path)
    today_str = datetime.today().strftime('%Y-%m-%d')
    print(f"Today's date: {today_str}")
    # Send prompt and image to Gemini for analysis
    prompt = {
        "text": (
            f"Today's date is {today_str}. "
            "Identify all food items in the image. For each item, extract:\n"
            "- The item name\n"
            "- The labeled expiration date (if present) in the format YYYY-MM-DD or as '<n> days'\n"
            "- The number of days until the product expires (from today)\n"
            "- The food category (e.g., Fruit, Vegetable, Meat, Dairy, etc.)\n"
            "If no label is present, estimate the number of days for the non-labeled items to expire. "
            "For each item, respond in the format:\n"
            "Item: <item>\nExpiration: <expiration text>\nCategory: <category>\n"
            "List each item on a new line."
        )
    }

    response = model.generate_content(contents=[prompt, im])
    items = []

    # Parse Gemini response text
    if response and response.candidates:
        # defensive access to parts
        parts = getattr(response.candidates[0].content, "parts", None)
        if parts and len(parts) > 0:
            text = parts[0].text
        else:
            text = ""
        print("Gemini raw response:\n", text)  # Debugging
        current_item = None
        current_exp = None
        current_cat = None
        for line in text.splitlines():
            if 'item' in line.lower():
                if current_item:
                    items.append({'item': current_item, 'expiration': current_exp, 'category': current_cat})
                current_item = line.split(':', 1)[-1].strip()
                current_exp = None
                current_cat = None
            elif 'expiration' in line.lower():
                current_exp = line.split(':', 1)[-1].strip()
            elif 'category' in line.lower():
                current_cat = line.split(':', 1)[-1].strip()
        if current_item:
            items.append({'item': current_item, 'expiration': current_exp, 'category': current_cat})

    # Fallback estimates / defaults
    for entry in items:
        if not entry.get('expiration') and entry.get('item'):
            expiry_info = estimate_expiration(entry['item'])
            entry['expiration'] = expiry_info
            print(f"Estimated expiry for {entry['item']}: {expiry_info}")
        if not entry.get('category'):
            entry['category'] = "Unknown"

    # Calculate days left and add to DB
    for entry in items:
        raw_exp = entry.get('expiration')
        print(f"Raw expiration string for '{entry['item']}': {raw_exp!r}")
        parsed_date = parse_expiration(raw_exp)
        print(f"Parsed date: {parsed_date}")
        if parsed_date:
            days_left = (parsed_date - datetime.today()).days
            if days_left < 0:
                days_left = 0
        else:
            # fallback when parse fails
            days_left = 7

        print(f"Item: {entry['item']}")
        print(f"Days before expiration: {days_left}")
        print(f"Category: {entry['category']}")
        add_food(entry['item'], days_left, entry['category'])

    return items


def parse_expiration(expiration_text):
    """Parse expiration text and return a datetime object."""
    if not expiration_text:
        return None
    
    today = datetime.today()
    expiration_text = expiration_text.lower().strip()
    
    import re
    
    try:
        # Handle formats like "2025-10-05 (7 days)" - extract the date part
        if '(' in expiration_text and ')' in expiration_text:
            # Extract the part before the parentheses
            date_part = expiration_text.split('(')[0].strip()
            # Try to parse the date part
            for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    return datetime.strptime(date_part, date_format)
                except ValueError:
                    continue
        
        # Try to parse standard date formats
        for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
            try:
                return datetime.strptime(expiration_text, date_format)
            except ValueError:
                continue
        
        # Parse "X days" format - extract number and add to today
        if 'day' in expiration_text:
            numbers = re.findall(r'\d+', expiration_text)
            if numbers:
                days = int(numbers[0])
                return today + timedelta(days=days)
        
        # Parse month abbreviations (e.g., "Oct 15", "Dec 2025")
        month_patterns = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        for month_name, month_num in month_patterns.items():
            if month_name in expiration_text:
                numbers = re.findall(r'\d+', expiration_text)
                if len(numbers) >= 1:
                    day = int(numbers[0]) if len(numbers) >= 1 else 1
                    year = int(numbers[1]) if len(numbers) >= 2 else today.year
                    try:
                        return datetime(year, month_num, day)
                    except ValueError:
                        pass
        
    except (ValueError, TypeError):
        pass
    
    return None


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        image_paths = sys.argv[1:]
    else:
        # Use absolute path relative to the project root
        project_root = os.path.dirname(os.path.dirname(__file__))
        image_paths = [os.path.join(project_root, "pictures", "full_fridge_test.jpg")]
        print("No images provided. Using default test image.")

    all_items = []
    for image_path in image_paths:
        print(f"Processing: {image_path}")
        items = analyze_image(image_path)
        all_items.extend(items)

    status_list = check_food_status()
    print("\nFood Status:")
    for name, status, category in status_list:
        print(f"{name}: {status}, category: {category}")
