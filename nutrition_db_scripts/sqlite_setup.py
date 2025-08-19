import pandas as pd
import sqlite3

# Load cleaned CSV
df = pd.read_csv("concise_foods_clean.csv")

# Optional: create a processed search column for robust searches
import re
df['food_name_search'] = df['food_name'].str.lower().str.replace(r'[^\w\s]', '', regex=True)

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("nutrition.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    energy REAL,
    protein REAL,
    fat REAL,
    carbohydrates REAL,
    food_name_search TEXT
)
""")

# Insert CSV data into SQLite
df.to_sql('foods', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
print("SQLite database 'nutrition.db' created and populated!")
