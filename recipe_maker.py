import os
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize AI model if API key is available
model = None
if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        print(f"Warning: Could not initialize Gemini API: {e}")
        model = None

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_user_foods(user_id=None, include_expiring_soon=True, days_threshold=3):
    """
    Get food items from the database for recipe generation.
    
    Args:
        user_id: If provided, gets user-specific foods. If None, gets general food inventory.
        include_expiring_soon: If True, prioritizes foods that are expiring soon
        days_threshold: Foods expiring within this many days are considered "expiring soon"
    
    Returns:
        List of tuples: (food_name, days_until_expiry, category/nutrition_info)
    """
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now()
    
    foods = []
    
    if user_id:
        # Get user-specific foods
        cursor.execute(
            "SELECT food_name, date_added, expire_days, nutrition FROM user_food WHERE user_id=?",
            (user_id,)
        )
    else:
        # Get general food inventory
        cursor.execute("SELECT name, date_added, expire_days, category FROM food")
    
    rows = cursor.fetchall()
    
    for row in rows:
        name = row[0]
        date_added = row[1]
        expire_days = row[2]
        extra_info = row[3] or ""
        
        try:
            date_added_dt = datetime.strptime(date_added, "%Y-%m-%d")
            expire_date = date_added_dt + timedelta(days=expire_days)
            days_left = (expire_date - today).days
            
            # Only include foods that haven't expired
            if days_left >= 0:
                foods.append((name, days_left, extra_info))
        except (ValueError, TypeError):
            # Skip invalid dates
            continue
    
    conn.close()
    
    # Sort by expiration date if prioritizing expiring foods
    if include_expiring_soon:
        foods.sort(key=lambda x: x[1])  # Sort by days_left (ascending)
    
    return foods

def get_expiring_foods(user_id=None, days_threshold=3):
    """Get foods that are expiring within the specified threshold."""
    all_foods = get_user_foods(user_id, include_expiring_soon=True)
    return [food for food in all_foods if food[1] <= days_threshold]

def make_recipe(food_items, recipe_size="medium", dietary_restrictions="", cuisine_preference=""):
    """
    Generate a recipe using the available food items.
    """
    if not food_items:
        return "No available food items to create a recipe."
    
    # Prepare food list with expiration info
    food_list = []
    expiring_soon = []
    
    for name, days_left, extra_info in food_items:
        if days_left <= 2:
            expiring_soon.append(f"{name} (expires in {days_left} days)")
        food_list.append(name)
    
    # Try AI generation first
    if model:
        try:
            # Enhanced prompt for better recipe generation
            prompt = f"""Create a delicious {cuisine_preference if cuisine_preference else 'international'} {recipe_size}-sized recipe using these available ingredients: {', '.join(food_list[:10])}.

{f"🚨 PRIORITY: Please prioritize these ingredients that are expiring soon: {', '.join(expiring_soon[:5])}" if expiring_soon else ""}

{f"📋 DIETARY REQUIREMENTS: {dietary_restrictions}" if dietary_restrictions else ""}

Please provide:
🍳 Creative and appetizing recipe name
📊 Serving size and difficulty level
📋 Complete ingredients list with estimated quantities
👨‍🍳 Clear step-by-step cooking instructions
⏱️ Estimated prep and cook time
💡 Chef's tips or variations

Make it tasty, practical for home cooking, and ensure all expiring ingredients are used effectively."""

            response = model.generate_content(prompt)
            if response and response.candidates:
                return response.candidates[0].content.parts[0].text
        except Exception as e:
            print(f"AI generation failed: {e}")
    
    # Fallback to simple recipe
    return generate_simple_recipe(food_list, expiring_soon, recipe_size, dietary_restrictions, cuisine_preference)

def generate_simple_recipe(food_list, expiring_soon, recipe_size="medium", dietary_restrictions="", cuisine_preference=""):
    """Generate a simple recipe when AI is not available."""
    if not food_list:
        return "No ingredients available for recipe generation."
    
    # Create a basic recipe with available ingredients
    recipe_name = f"{cuisine_preference} {recipe_size} Recipe" if cuisine_preference else f"Simple {recipe_size} Recipe"
    
    # Format the output
    result = f"🍳 **{recipe_name}**\n\n"
    result += f"📊 **Recipe Size:** {recipe_size.title()}\n"
    
    if dietary_restrictions:
        result += f"🥗 **Dietary Notes:** {dietary_restrictions}\n"
    
    if cuisine_preference:
        result += f"🌍 **Cuisine Style:** {cuisine_preference}\n"
    
    result += f"\n📋 **Ingredients:**\n"
    for i, ingredient in enumerate(food_list[:8], 1):
        result += f"{i}. {ingredient.title()}\n"
    
    if expiring_soon:
        result += f"\n⏰ **Use These First (Expiring Soon):**\n"
        for item in expiring_soon:
            result += f"• {item}\n"
    
    result += f"\n👨‍🍳 **Instructions:**\n"
    result += "1. Prepare all ingredients by washing and chopping as needed\n"
    result += "2. Heat oil in a pan if available\n"
    result += "3. Cook ingredients starting with those that take longest\n"
    result += "4. Combine everything and season to taste\n"
    result += "5. Cook until everything is heated through and tender\n"
    result += "6. Serve while hot\n"
    
    result += f"\n⏱️ **Estimated Cooking Time:** 20-30 minutes\n"
    result += f"\n💡 **Note:** This recipe was generated using available ingredients. Adjust quantities and seasonings to taste!"
    
    return result

def make_recipe_for_user(user_id, recipe_size="medium", dietary_restrictions="", cuisine_preference="", prioritize_expiring=True):
    """Generate a recipe specifically for a user's food inventory."""
    food_items = get_user_foods(user_id, include_expiring_soon=prioritize_expiring)
    return make_recipe(food_items, recipe_size, dietary_restrictions, cuisine_preference)

def make_recipe_from_general_inventory(recipe_size="medium", dietary_restrictions="", cuisine_preference="", prioritize_expiring=True):
    """Generate a recipe from the general food inventory."""
    food_items = get_user_foods(None, include_expiring_soon=prioritize_expiring)
    return make_recipe(food_items, recipe_size, dietary_restrictions, cuisine_preference)

if __name__ == '__main__':
    # Test the recipe generation
    print("=== ExpirEase Recipe Generator ===\n")
    
    try:
        recipe = make_recipe_from_general_inventory(prioritize_expiring=True)
        print("Generated Recipe:")
        print(recipe)
    except Exception as e:
        print(f"Error generating recipe: {e}")
        
    print("\n" + "="*50)
