# search_foods.py
import os
import psycopg
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_similar_foods(query, top_n=1):
    """Return top_n foods most similar to the query string."""
    
    # Generate embedding for the user query
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vector = resp.data[0].embedding

    # Connect to Postgres
    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    ) as conn:
        with conn.cursor() as cur:
            # Run similarity search using pgvector
            cur.execute("""
                SELECT food_name, food_name_search, energy
                FROM foods
                ORDER BY embedding <-> %s::vector
                LIMIT %s;
            """, (query_vector, top_n))


            
            
            results = cur.fetchall()
    
    return results

# Example usage
if __name__ == "__main__":
    query = "chicken breast raw"
    top_foods = search_similar_foods(query)
    for food_name, search_name, energy in top_foods:
        print(f"{food_name} → {search_name}, calories: {energy}")
