import pandas as pd

# --- CONFIGURATION ---
input_file = "nz_nutrition_concise.csv"  # path to your Concise CSV
output_file = "concise_foods_clean.csv"

# Columns to keep (match your CSV)
columns_to_keep = [
    'short food name',       # food description
    'energy',                # energy per 100g
    'protein',               # protein per 100g
    'fat',                   # fat per 100g
    'carbohydrate, available'  # carbs per 100g
]

# --- LOAD DATA ---
df = pd.read_csv(input_file, encoding="latin1")  # adjust encoding if needed

# --- CLEAN COLUMN NAMES ---
df.columns = df.columns.str.strip().str.lower()  # remove spaces, lowercase

# --- KEEP ONLY RELEVANT COLUMNS ---
columns_existing = [col for col in columns_to_keep if col in df.columns]
df_clean = df[columns_existing].copy()  # make a proper copy to avoid warnings

# --- RENAME COLUMNS ---
df_clean.rename(columns={
    'short food name': 'food_name',
    'carbohydrate, available': 'carbohydrates'
}, inplace=True)

# --- CLEAN FOOD NAMES ---
df_clean['food_name'] = df_clean['food_name'].str.strip().str.title()

# --- REMOVE ROWS WITH NO USEFUL MACRO DATA ---
# Drop rows where all macro columns are NaN
df_clean = df_clean.dropna(subset=['energy', 'protein', 'fat', 'carbohydrates'], how='all')

# Remove rows where all macros are zero
df_clean = df_clean[~((df_clean['energy'] == 0) &
                      (df_clean['protein'] == 0) &
                      (df_clean['fat'] == 0) &
                      (df_clean['carbohydrates'] == 0))]

# --- SAVE CLEAN CSV ---
df_clean.to_csv(output_file, index=False)
print(f"Clean CSV saved to: {output_file}")
print(f"Number of foods with nutrient data: {len(df_clean)}")

# --- SEARCH FUNCTION ---
def search_food(term):
    """Search for a food by name (case-insensitive)."""
    results = df_clean[df_clean['food_name'].str.contains(term, case=False, na=False)]
    return results

# --- EXAMPLE SEARCH ---
search_term = "chicken breast"  # try "potato" or any food
results = search_food(search_term)

if results.empty:
    print(f"No results found for '{search_term}'")
else:
    print(f"Results for '{search_term}':")
    print(results)
