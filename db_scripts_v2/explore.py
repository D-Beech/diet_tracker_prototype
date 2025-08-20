import pandas as pd 
from pandas import read_csv

#using dataset from here

# ## 📦 Source

# Original raw data: [OpenFoodFacts](https://world.openfoodfacts.org/data)

# This data still needs additional processing, lower_case, deduplicate

# might be better to go from og source but this will do for mvp

path = 'nutrition_selected_final.csv'

df = read_csv(path)

df = df[['product_name', 'energy-kcal_100g', 'fat_100g', 'proteins_100g', 'carbohydrates_100g']]

pd.set_option('display.max_columns', 5)  # Show max 5 columns

pd.set_option('display.max_colwidth', 20)  # Limit max characters per column
# print(df.head())

# print(df.columns)
df_chicken = df[df['product_name'] == 'Banana']

print(df_chicken.head())

print(df.columns)


