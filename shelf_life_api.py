# shelf_life_api.py
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def get_expiry_from_stilltasty(food_name):
    """
    Fetches expiry information for a given food item from StillTasty.com.
    Returns a string with the expiry info, or None if not found.
    """
    search_url = f"https://www.stilltasty.com/searchitems/search?search={food_name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        search_resp = requests.get(search_url, headers=headers, timeout=10)
        search_resp.raise_for_status()
        soup = BeautifulSoup(search_resp.text, "html.parser")
        result_link = soup.select_one(".search-results .media-body a")
        if not result_link or not result_link.get("href"):
            return None
        food_url = "https://www.stilltasty.com" + result_link.get("href")
        food_resp = requests.get(food_url, headers=headers, timeout=10)
        food_resp.raise_for_status()
        food_soup = BeautifulSoup(food_resp.text, "html.parser")
        answer = food_soup.select_one(".answer")
        if answer:
            return answer.get_text(strip=True)
        summary = food_soup.select_one(".summary")
        if summary:
            return summary.get_text(strip=True)
        return None
    except Exception as e:
        print(f"Error fetching from StillTasty: {e}")
        return None

def estimate_expiration(item):
    today = datetime.today()
    item = item.lower()

    try:
        url = f"https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": item,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 1
        }
        resp = requests.get(url, params=params)
        data = resp.json()

        if data.get("products"):
            product = data["products"][0]
            categories = product.get("categories", "").lower()

            if "banana" in categories or "grape" in categories:
                return (today + timedelta(days=5)).strftime('%Y-%m-%d')
            elif "candy" in categories or "chocolate" in categories:
                return (today + timedelta(days=30)).strftime('%Y-%m-%d')
            elif "apple" in categories or "pear" in categories:
                return (today + timedelta(days=21)).strftime('%Y-%m-%d')
            else:
                # Try StillTasty for more info
                stilltasty_info = get_expiry_from_stilltasty(item)
                if stilltasty_info:
                    return stilltasty_info
                return (today + timedelta(days=7)).strftime('%Y-%m-%d')
        else:
            # Try StillTasty if OpenFoodFacts has no product
            stilltasty_info = get_expiry_from_stilltasty(item)
            if stilltasty_info:
                return stilltasty_info
    except Exception as e:
        print("Error using external API:", e)

    # Fallback default
    return (today + timedelta(days=7)).strftime('%Y-%m-%d')