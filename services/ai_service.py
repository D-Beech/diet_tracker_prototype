from openai import OpenAI
import json

def do_ai(prompt, api_key):
    client = OpenAI(api_key=api_key)

    schema_instruction = """
    Please respond ONLY in JSON matching this schema:

    {
    "exercise": [
        {
        "name": "string",
        "sets": number,          // optional for cardio
        "reps": number,          // optional for cardio
        "weight_kg": number,     // optional, can be null for bodyweight
        "distance_km": number,   // optional, for running/cycling
        "time_min": number       // optional, for running/cycling
        }
    ],
    "food": [
        {
        "name": "string",
        "quantity_g": number,      // optional if quantity_items is provided
        "quantity_items": number   // optional if quantity_g is provided
        }
    ],
    "body_weight_kg": number
    }

    Rules:
    1. Use numbers only in the fields above. Do NOT add text.
    2. Ignore unrelated information (like Pokémon).
    3. Convert approximate units to the most natural one (grams for solid food if specified, otherwise number of items).
    4. Always extract exercises exactly as described: sets, reps, and weight (or distance/time for cardio).
    5. Respond with VALID JSON only, no extra commentary.
    6. If a field is not specified, use null.
    """


    full_prompt = f"{prompt}\n\n{schema_instruction}"

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )
        # Parse the JSON
        response_text = completion.choices[0].message.content
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"error": "AI did not return valid JSON", "raw_response": response_text}
    except Exception as e:
        return {"error": str(e)}
