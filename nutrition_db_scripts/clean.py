import pandas as pd

input_file = "en.openfoodfacts.org.products.csv"
output_file = "nutrition_cleaned.csv"

# Keep only relevant columns
cols = [
    "product_name", "brands", 
    "energy_100g", "proteins_100g", 
    "carbohydrates_100g", "fat_100g"
]

# Chunking is required to run this job on my 16gb laptop
chunksize = 100_000
first = True

for chunk in pd.read_csv(input_file, sep="\t", usecols=cols, chunksize=chunksize, low_memory=False):

    # Drop rows where any required field is missing
    chunk = chunk.dropna(subset=cols)

    # Convert to numeric safely
    for col in ["energy_100g", "proteins_100g", "carbohydrates_100g", "fat_100g"]:
        chunk[col] = pd.to_numeric(chunk[col], errors="coerce", downcast="float")

    # Drop again if conversion introduced NaNs
    chunk = chunk.dropna(subset=["energy_100g", "proteins_100g", "carbohydrates_100g", "fat_100g"])

    # Filter impossible values
    chunk = chunk[
        (chunk["energy_100g"] > 0) & (chunk["energy_100g"] < 4000) &
        (chunk["proteins_100g"] >= 0) & (chunk["proteins_100g"] <= 100) &
        (chunk["carbohydrates_100g"] >= 0) & (chunk["carbohydrates_100g"] <= 100) &
        (chunk["fat_100g"] >= 0) & (chunk["fat_100g"] <= 100)
    ]

    # Drop duplicates (name + brand + macros)
    chunk = chunk.drop_duplicates(subset=cols)

    # Save cleaned chunk to CSV (append after first chunk)
    chunk.to_csv(output_file, mode="a", index=False, header=first)
    first = False
