# pg_generate_embeddings_batch_fixed.py
import os
import psycopg
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()  # ensure your API key is loaded

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BATCH_SIZE = 50  # adjust for speed vs memory

with psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
) as conn:
    with conn.cursor() as cur:
        # Fetch all rows without embeddings
        cur.execute("""
            SELECT id, food_name_search
            FROM foods
            WHERE embedding IS NULL;
        """)
        rows = cur.fetchall()
        print(f"{len(rows)} rows to process...")

        for i in range(0, len(rows), BATCH_SIZE):
            batch = rows[i:i+BATCH_SIZE]

            # Filter out empty texts
            batch_items = [(r[0], str(r[1])) for r in batch if r[1] and str(r[1]).strip() != ""]
            if not batch_items:
                continue

            ids, texts = zip(*batch_items)

            resp = client.embeddings.create(
                model="text-embedding-3-small",
                input=list(texts)
            )
            embeddings = [e.embedding for e in resp.data]

            for row_id, emb in zip(ids, embeddings):
                cur.execute(
                    "UPDATE foods SET embedding = %s WHERE id = %s",
                    (emb, row_id)
                )

            conn.commit()
            print(f"Processed rows {i+1}-{i+len(batch_items)}")


print("✅ All embeddings generated and saved in Postgres!")
