import sqlite3
import re

# --- CONFIGURATION ---
db_file = "nutrition.db"  # SQLite database file
user_input = "chicken breast"  # Example user input

# --- SMALL CANONICAL MAPPING ---
canonical_map = {
    "chicken": "chicken, breast, lean, fresh, baked or roasted, no fat or salt added",
    "plain chicken": "chicken, breast, lean, fresh, baked or roasted, no fat or salt added",
    "chicken breast": "chicken, breast, lean, fresh, baked or roasted, no fat or salt added",
    "potato": "potato, flesh, floury, boiled, no salt added",
}

# --- RESOLVE CANONICAL FOOD NAME ---
canonical_food = canonical_map.get(user_input.lower(), user_input)

# --- PREPROCESS SEARCH TERMS ---
keywords = re.sub(r'[^\w\s]', '', canonical_food.lower()).split()

# --- CONNECT TO DATABASE ---
conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row  # Access columns by name
cursor = conn.cursor()

# --- FETCH ALL FOODS ---
cursor.execute("SELECT food_name, energy, protein, fat, carbohydrates, food_name_search FROM foods")
all_rows = cursor.fetchall()
conn.close()

# --- KEYWORD-BASED SEARCH (SAFE FOR NULLS) ---
results = []
for row in all_rows:
    food_search = row['food_name_search'] or ""  # Replace None with empty string
    if all(kw in food_search for kw in keywords):
        results.append(row)

# --- DISPLAY RESULTS ---
if results:
    print(f"Results for '{user_input}' (mapped to '{canonical_food}'):\n")
    for row in results:
        print(f"Food: {row['food_name']}")
        print(f"Energy: {row['energy']} kcal, Protein: {row['protein']} g, Fat: {row['fat']} g, Carbs: {row['carbohydrates']} g")
        print("-" * 50)
else:
    print(f"No results found for '{user_input}' (mapped to '{canonical_food}')")
