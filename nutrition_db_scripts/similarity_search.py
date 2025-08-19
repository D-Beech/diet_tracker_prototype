# similarity_search_filtered.py
import os
import psycopg
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_similar_foods(query, top_n=5):
    """
    Search for top N foods matching the query using:
    1. Keyword filter
    2. Embedding similarity ranking
    """
    # Generate query embedding
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vector = resp.data[0].embedding

    # Extract keywords from query (simple split, lowercase)
    keywords = [w.lower() for w in query.split() if w.strip() != ""]

    # Connect to Postgres
    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    ) as conn:
        with conn.cursor() as cur:
            # Build parameterized keyword filter
            keyword_conditions = []
            params = []
            for k in keywords:
                keyword_conditions.append("food_name_search ILIKE %s")
                params.append(f"%{k}%")

            keyword_filter = " AND ".join(keyword_conditions)

            sql = f"""
                SELECT food_name, food_name_search, energy
                FROM foods
                WHERE {keyword_filter}
                ORDER BY embedding <-> %s::vector
                LIMIT %s;
            """
            # Append embedding vector and limit to params
            params.extend([query_vector, top_n])

            cur.execute(sql, params)
            results = cur.fetchall()

    return results

# Example usage
if __name__ == "__main__":
    query = "chicken breast"
    top_foods = search_similar_foods(query)
    for food_name, search_name, energy in top_foods:
        print(f"{food_name} → {search_name}, Calories: {energy}")

