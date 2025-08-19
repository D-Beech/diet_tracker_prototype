# migration.py
import sqlite3
import psycopg
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Path to SQLite DB in the same folder as this script
sqlite_db_path = os.path.join(os.path.dirname(__file__), "nutrition.db")

# SQLite connection
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cur = sqlite_conn.cursor()

# Postgres connection
pg_conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
pg_cur = pg_conn.cursor()

# Create table in Postgres if it doesn't exist
pg_cur.execute("""
CREATE TABLE IF NOT EXISTS foods (
    food_name TEXT,
    energy TEXT,
    protein TEXT,
    fat TEXT,
    carbohydrates TEXT,
    food_name_search TEXT
);
""")
pg_conn.commit()

# Fetch all rows from SQLite
sqlite_cur.execute("SELECT * FROM foods;")
rows = sqlite_cur.fetchall()

# Insert rows into Postgres
columns = ["food_name", "energy", "protein", "fat", "carbohydrates", "food_name_search"]
columns_str = ", ".join(columns)
placeholders = ", ".join(["%s"] * len(columns))

insert_query = f"INSERT INTO foods ({columns_str}) VALUES ({placeholders})"
pg_cur.executemany(insert_query, rows)
pg_conn.commit()

# Close connections
sqlite_conn.close()
pg_cur.close()
pg_conn.close()

print(f"✅ Migrated {len(rows)} rows from SQLite to Postgres!")
