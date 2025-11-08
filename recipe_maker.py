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
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        
        # Try gemini-1.5-pro for better recipe generation (different model than scanner)
        model = genai.GenerativeModel(
            'gemini-1.5-pro',  # Pro model may have different safety filters
            generation_config={
                'temperature': 1.2,      # High creativity for unique recipes
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            },
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        print("Recipe AI model initialized successfully")
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
    Tries AI first for variety, falls back to template if AI fails.
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
            import random
            
            # Select up to 8 ingredients
            ingredients = food_list[:8]
            
            # Create a simple, natural prompt that shouldn't trigger filters
            prompt = f"""Create a delicious {recipe_size} serving meal using these ingredients: {', '.join(ingredients)}.

Format your response exactly like this:

**[Creative Recipe Name]**

**Servings:** {recipe_size.capitalize()} | **Time:** [X] minutes

**Ingredients:**
- [ingredient 1] - [specific amount]
- [ingredient 2] - [specific amount]
(list all with measurements)

**Instructions:**
1. [First step with timing]
2. [Second step with timing]
(detailed steps)

**Chef's Tip:** [One helpful cooking tip]

**Variations:** [2-3 ways to customize]"""

            if dietary_restrictions:
                prompt += f"\n\nDietary requirements: {dietary_restrictions}"
            if cuisine_preference:
                prompt += f"\nCuisine style: {cuisine_preference}"
            if expiring_soon:
                prompt += f"\n\nPriority: Use these ingredients first as they're expiring soon: {', '.join(expiring_soon[:3])}"
            
            print(f"Attempting AI recipe generation with {len(ingredients)} ingredients...")
            
            # Generate with timeout
            response = model.generate_content(
                prompt,
                request_options={'timeout': 20}
            )
            
            # Check response
            if response and response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                
                # Check if we got actual content
                if candidate.finish_reason == 1 and candidate.content and candidate.content.parts:
                    recipe = candidate.content.parts[0].text
                    if recipe and len(recipe) > 100:  # Make sure we got a real recipe
                        print(f"✓ AI recipe generated successfully ({len(recipe)} chars)")
                        return recipe
                    else:
                        print("✗ AI response too short, using fallback")
                else:
                    print(f"✗ AI blocked (reason: {candidate.finish_reason}), using fallback")
            else:
                print("✗ No AI response, using fallback")
                
        except Exception as e:
            print(f"✗ AI generation error: {e}")
    
    # Fallback to template-based generator
    print(f"Using template recipe generator with {len(food_list)} ingredients")
    return generate_simple_recipe(food_list, expiring_soon, recipe_size, dietary_restrictions, cuisine_preference)

def generate_simple_recipe(food_list, expiring_soon, recipe_size="medium", dietary_restrictions="", cuisine_preference=""):
    """Generate a detailed recipe with specific measurements and instructions."""
    print(f"DEBUG: generate_simple_recipe called with {len(food_list) if food_list else 0} ingredients")
    
    if not food_list:
        return "No ingredients available for recipe generation."
    
    import random
    
    # Categorize ingredients
    fruits = []
    vegetables = []
    proteins = []
    grains = []
    dairy = []
    others = []
    
    for item in food_list[:8]:
        item_lower = item.lower()
        if any(fruit in item_lower for fruit in ['apple', 'banana', 'grape', 'berry', 'strawberry', 'orange', 'lemon', 'melon']):
            fruits.append(item)
        elif any(veg in item_lower for veg in ['lettuce', 'spinach', 'kale', 'carrot', 'pepper', 'tomato', 'cucumber', 'asparagus', 'broccoli', 'cauliflower', 'green']):
            vegetables.append(item)
        elif any(protein in item_lower for protein in ['chicken', 'beef', 'pork', 'fish', 'egg', 'tofu', 'bean']):
            proteins.append(item)
        elif any(grain in item_lower for grain in ['rice', 'pasta', 'bread', 'oat', 'cereal', 'tortilla', 'quinoa']):
            grains.append(item)
        elif any(d in item_lower for d in ['milk', 'cheese', 'yogurt', 'cream', 'butter']):
            dairy.append(item)
        else:
            others.append(item)
    
    # Determine recipe type based on ingredients
    if fruits and (grains or dairy or 'oat' in ' '.join(food_list).lower()):
        recipe_type = "Breakfast Bowl"
        recipe_name = random.choice([
            "Berry & Oat Breakfast Bowl",
            "Fruit Parfait Delight",
            "Morning Power Bowl",
            "Fresh Fruit Breakfast"
        ])
        
        result = f"🍳 **{recipe_name}**\n\n"
        result += f"📊 **Servings:** {recipe_size.title()} (2-3 portions) | ⏱️ **Total Time:** 10 minutes\n\n"
        
        result += "📋 **INGREDIENTS:**\n"
        if grains:
            result += f"• {grains[0]} - 1 cup\n"
        if dairy:
            result += f"• {dairy[0]} - 1/2 cup\n"
        for fruit in fruits[:3]:
            result += f"• {fruit} - 1/2 cup, chopped\n"
        result += "• Honey or maple syrup - 1-2 tablespoons\n"
        result += "• Cinnamon - 1/4 teaspoon (optional)\n"
        
        result += "\n👨‍🍳 **INSTRUCTIONS:**\n\n"
        result += "**Step 1: Prepare Base**\n"
        if 'oat' in ' '.join(grains).lower():
            result += "Cook oats according to package directions (typically 1 cup oats with 2 cups water/milk, simmer 5 minutes)\n\n"
        else:
            result += f"Prepare your base ({grains[0] if grains else 'grains'}) according to package directions\n\n"
        
        result += "**Step 2: Prep Fruits** (3 minutes)\n"
        result += "While base cooks, wash and chop all fruits into bite-sized pieces (about 1/2 inch cubes)\n\n"
        
        result += "**Step 3: Assemble** (2 minutes)\n"
        result += "Layer in bowls: base on bottom, add yogurt or milk if using, top with fresh fruits\n\n"
        
        result += "**Step 4: Finish**\n"
        result += "Drizzle with honey/syrup, sprinkle cinnamon on top\n"
        result += "Serve immediately while base is warm and fruits are fresh\n\n"
        
        result += "💡 **CHEF'S TIP:** Layer fruits by color for an Instagram-worthy presentation!\n"
        
    elif vegetables and (proteins or grains):
        recipe_type = "Stir-Fry or Salad"
        recipe_name = random.choice([
            "Garden Fresh Stir-Fry",
            "Crispy Vegetable Medley",
            "Power Veggie Bowl",
            "Fresh Garden Salad"
        ])
        
        result = f"🍳 **{recipe_name}**\n\n"
        result += f"📊 **Servings:** {recipe_size.title()} (2-3 portions) | ⏱️ **Prep:** 10 min | **Cook:** 15 min\n\n"
        
        result += "📋 **INGREDIENTS:**\n"
        for veg in vegetables[:4]:
            result += f"• {veg} - 1 cup, chopped\n"
        if proteins:
            result += f"• {proteins[0]} - 8 oz (about 2 cups diced)\n"
        result += "• Olive oil - 2 tablespoons\n"
        result += "• Garlic - 2 cloves, minced\n"
        result += "• Salt - 1/2 teaspoon\n"
        result += "• Black pepper - 1/4 teaspoon\n"
        result += "• Soy sauce or lemon juice - 2 tablespoons\n"
        
        result += "\n👨‍🍳 **INSTRUCTIONS:**\n\n"
        result += "**Step 1: Prep Work** (5-8 minutes)\n"
        result += "• Wash all vegetables thoroughly under cold water\n"
        result += "• Chop vegetables into uniform 1-inch pieces for even cooking\n"
        result += "• Mince garlic finely\n"
        if proteins:
            result += f"• Cut {proteins[0]} into 1-inch cubes\n\n"
        
        result += "**Step 2: Heat Pan** (2 minutes)\n"
        result += "Heat a large skillet or wok over medium-high heat (about 375°F)\n"
        result += "Add 2 tablespoons olive oil, swirl to coat\n"
        result += "Oil should shimmer but not smoke\n\n"
        
        result += "**Step 3: Cook Proteins** (6-8 minutes)\n" if proteins else "**Step 3: Sauté Aromatics** (1 minute)\n"
        if proteins:
            result += f"Add {proteins[0]}, spread in single layer\n"
            result += "Don't move for 2-3 minutes to get a nice sear\n"
            result += "Flip and cook other side until golden brown and cooked through\n"
            result += "Remove to plate\n\n"
            result += "**Step 4: Cook Vegetables** (5-7 minutes)\n"
        else:
            result += "**Step 4: Cook Vegetables** (7-10 minutes)\n"
        
        result += "Add minced garlic, stir for 30 seconds until fragrant\n"
        result += "Add harder vegetables first (carrots, peppers), stir-fry 3 minutes\n"
        result += "Add softer vegetables (greens, tomatoes), stir-fry 2-3 minutes more\n"
        result += "Vegetables should be tender-crisp with some browning\n\n"
        
        result += "**Step 5: Combine & Season** (2 minutes)\n"
        if proteins:
            result += f"Return {proteins[0]} to pan\n"
        result += "Add soy sauce/lemon juice, salt, and pepper\n"
        result += "Toss everything together for 1-2 minutes to heat through\n"
        result += "Taste and adjust seasoning\n\n"
        
        result += "**Step 6: Serve**\n"
        result += f"Serve hot over {grains[0] if grains else 'rice or quinoa'}\n"
        result += "Garnish with fresh herbs if available\n\n"
        
        result += "💡 **CHEF'S TIP:** Don't overcrowd the pan - cook in batches if needed for best browning!\n"
        
    else:
        # Default mixed recipe
        recipe_name = random.choice([
            "Kitchen Remix Bowl",
            "Creative Combo Plate",
            "Fresh Mix Delight",
            "Whatever's Fresh Bowl"
        ])
        
        result = f"🍳 **{recipe_name}**\n\n"
        result += f"📊 **Servings:** {recipe_size.title()} | ⏱️ **Total Time:** 20 minutes\n\n"
        
        result += "📋 **INGREDIENTS:**\n"
        for i, ingredient in enumerate(food_list[:8], 1):
            # Add realistic measurements
            if i <= 3:
                result += f"• {ingredient} - 1 cup\n"
            else:
                result += f"• {ingredient} - 1/2 cup\n"
        result += "• Olive oil - 2 tablespoons\n"
        result += "• Salt and pepper - to taste\n"
        result += "• Optional: garlic powder, onion powder, herbs - 1 teaspoon each\n"
        
        result += "\n👨‍🍳 **INSTRUCTIONS:**\n\n"
        result += "**Step 1: Mise en Place** (5 minutes)\n"
        result += "Gather and prep all ingredients:\n"
        result += "• Wash produce thoroughly\n"
        result += "• Chop everything into bite-sized pieces (about 1 inch)\n"
        result += "• Arrange ingredients in order of cooking time needed\n\n"
        
        result += "**Step 2: Start Cooking** (3 minutes)\n"
        result += "Heat large pan over medium-high heat (350-375°F)\n"
        result += "Add 2 tablespoons oil, let heat until shimmering (about 1 minute)\n\n"
        
        result += "**Step 3: Layer Cook** (8-10 minutes)\n"
        result += "Add ingredients starting with those taking longest:\n"
        result += "• Dense items (root vegetables, proteins): cook 5-6 minutes\n"
        result += "• Medium items (most vegetables): add and cook 3-4 minutes\n"
        result += "• Quick items (greens, herbs): add last, cook 1-2 minutes\n"
        result += "Stir frequently to prevent sticking\n\n"
        
        result += "**Step 4: Season & Finish** (2 minutes)\n"
        result += "Add salt (start with 1/2 teaspoon), pepper (1/4 teaspoon)\n"
        result += "Add any additional seasonings\n"
        result += "Toss well, cook 1 more minute\n"
        result += "Taste and adjust seasoning\n\n"
        
        result += "**Step 5: Plate & Serve**\n"
        result += "Transfer to serving bowls while hot\n"
        result += "Drizzle with extra olive oil or a squeeze of lemon if desired\n\n"
        
        result += "💡 **CHEF'S TIP:** The key is high heat and not overcrowding - give ingredients room to breathe!\n"
    
    if expiring_soon:
        result += f"\n⏰ **PRIORITY INGREDIENTS** (Use first - expiring soon):\n"
        for item in expiring_soon[:3]:
            result += f"• {item}\n"
    
    result += f"\n🌟 **VARIATIONS:**\n"
    result += "• Add your favorite seasonings (curry powder, Italian herbs, etc.)\n"
    result += "• Swap cooking methods: grill, roast, or steam instead of sauté\n"
    result += "• Add a protein or grain to make it more filling\n"
    
    print(f"DEBUG: Returning recipe with length {len(result)} characters")
    print(f"DEBUG: Recipe preview: {result[:200]}...")
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
