import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

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

def parse_days_from_text(text):
    """
    Extracts the average number of days from a string like '3-5 days' or '7 days'.
    Returns the average days as an integer, or None if not found.
    """
    match = re.search(r'(\d+)(?:-(\d+))?\s+days?', text)
    if match:
        min_days = int(match.group(1))
        max_days = int(match.group(2)) if match.group(2) else min_days
        avg_days = (min_days + max_days) // 2
        return avg_days
    return None

def estimate_expiration(item):
    """
    Estimates the expiration date for any food using StillTasty.
    Returns a date string (YYYY-MM-DD) if possible, otherwise a descriptive string or None.
    """
    today = datetime.today()
    stilltasty_info = get_expiry_from_stilltasty(item)
    if stilltasty_info:
        days = parse_days_from_text(stilltasty_info)
        if days:
            return (today + timedelta(days=days)).strftime('%Y-%m-%d')
        return stilltasty_info  # fallback to text if parsing fails
    # Fallback default if nothing found
    return (today + timedelta(days=7)).strftime('%Y-%m-%d')