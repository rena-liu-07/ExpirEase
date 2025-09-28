import os
import re
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
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def parse_expiration(exp_str: str):
    """
    Robustly parse expiration information from strings like:
      - "2025-10-10"
      - "Expires 2025-10-10 (in 5 days)"
      - "10/10/2025"
      - "in 5 days", "5 days"
      - "2 weeks", "3 months"
      - "5"  (interpreted as days but only if reasonable)
    Returns a datetime object or None if parsing fails.
    """
    if not exp_str:
        return None

    s = exp_str.strip().lower()

    # 1) Find ISO-like date YYYY-MM-DD or YYYY/MM/DD anywhere in the string
    iso_match = re.search(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', s)
    if iso_match:
        date_str = iso_match.group(1).replace('/', '-')
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            pass

    # 2) Find MM/DD/YYYY or MM-DD-YYYY
    md_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})', s)
    if md_match:
        date_str = md_match.group(1)
        for fmt in ("%m-%d-%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(date_str, fmt)
            except Exception:
                pass

    # 3) Relative times: days, weeks, months
    # days
    days_match = re.search(r'(\d+)\s*(?:day|days|d)\b', s)
    if days_match:
        days = int(days_match.group(1))
        return datetime.today() + timedelta(days=days)

    # weeks
    weeks_match = re.search(r'(\d+)\s*(?:week|weeks|w)\b', s)
    if weeks_match:
        weeks = int(weeks_match.group(1))
        return datetime.today() + timedelta(weeks=weeks)

    # months (approximate a month as 30 days)
    months_match = re.search(r'(\d+)\s*(?:month|months)\b', s)
    if months_match:
        months = int(months_match.group(1))
        return datetime.today() + timedelta(days=30 * months)

    # 4) If the whole string is a simple integer (e.g. "5"), treat as days
    num_full = re.fullmatch(r'\d+', s)
    if num_full:
        n = int(s)
        # guard against interpreting years (e.g. "2025") as days
        if n <= 365:
            return datetime.today() + timedelta(days=n)
        # otherwise treat as invalid (None) so fallback logic will be used
        return None

    # 5) Last resort: look for any reasonable small integer anywhere (but avoid years)
    # This avoids catching a year from a date like 2025-10-10 because we've already matched dates above.
    loose_num = re.search(r'(\d+)', s)
    if loose_num:
        n = int(loose_num.group(1))
        if 0 < n <= 365:
            return datetime.today() + timedelta(days=n)

    return None


def analyze_image(image_path):
    # Open image safely
    im = Image.open(image_path)
    today_str = datetime.today().strftime('%Y-%m-%d')

    # Prompt Gemini
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


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        image_paths = sys.argv[1:]
    else:
        image_paths = ["pictures/full_fridge_test.jpg"]
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
