import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_food_items(file_path):
    with open(file_path, 'r') as f:
        items = [line.strip() for line in f if line.strip()]
    return items

def make_recipe(food_items):
    prompt = {
        "text": (
            "Given the following list of food items, create a simple but delicious recipe using as many of them as possible. "
            "List the recipe name, ingredients, and step-by-step instructions. "
            "Food items: " + ', '.join(food_items)
        )
    }
    response = model.generate_content(contents=[prompt])
    if response and response.candidates:
        return response.candidates[0].content.parts[0].text
    return "No recipe generated."

if __name__ == '__main__':
    items_file = 'food_items.txt'  # Replace with your file containing food items
    food_items = get_food_items(items_file)
    recipe = make_recipe(food_items)
    print(recipe)
