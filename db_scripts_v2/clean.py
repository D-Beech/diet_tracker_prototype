import pandas as pd

# --- CONFIG ---
input_csv = 'nutrition_selected_final.csv'  # original file
output_csv = 'nutrition_cleaned.csv'        # cleaned file
columns_to_keep = ['product_name', 'energy-kcal_100g', 'proteins_100g', 'fat_100g', 'carbohydrates_100g']

# --- LOAD CSV (only needed columns to save memory) ---
df = pd.read_csv(input_csv, usecols=columns_to_keep)

# --- CLEANING ---
# Convert product names to lowercase
df['product_name'] = df['product_name'].str.lower().str.strip()

# Remove duplicates based on product name
df = df.drop_duplicates(subset=['product_name'])

# Optional: rename columns to shorter names for MVP
df = df.rename(columns={
    'energy-kcal_100g': 'kcal',
    'proteins_100g': 'protein',
    'fat_100g': 'fat',
    'carbohydrates_100g': 'carbs'
})

# --- SAVE CLEANED CSV ---
df.to_csv(output_csv, index=False)

print(f"Cleaned CSV saved to '{output_csv}' with {len(df)} unique products.")
