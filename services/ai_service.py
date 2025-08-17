# services/ai_service.py
from openai import OpenAI
from .models import LogEntry
import json
from datetime import datetime

def do_ai(prompt, api_key, log_time: datetime = None):
    """
    :param prompt: User input
    :param api_key: OpenAI API key
    :param log_time: Optional datetime provided by user for the log
    """
    client = OpenAI(api_key=api_key)

    schema_instruction = """
    Please respond ONLY in JSON matching this schema:

    {
      "exercise": [
        {
          "name": "string",
          "sets": number,
          "reps": number,
          "weight_kg": number,
          "distance_km": number,
          "time_min": number
        }
      ],
      "food": [
        {
          "name": "string",
          "quantity_g": number,
          "quantity_items": number
        }
      ],
      "body_weight_kg": number
    }

    Rules:
    1. Use numbers only in the fields above. Do NOT add text.
    2. Ignore unrelated information.
    3. Convert approximate units to the most natural one.
    4. Always extract exercises exactly as described.
    5. Respond with VALID JSON only, no extra commentary.
    6. If a field is not specified, use null.
    """

    full_prompt = f"{prompt}\n\n{schema_instruction}"

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )

        response_text = completion.choices[0].message.content

        # Parse JSON first
        parsed_json = json.loads(response_text)

        # Inject the timestamp from request if provided
        if log_time:
            parsed_json["timestamp"] = log_time.isoformat()

        # Validate and parse with Pydantic
        validated_data = LogEntry.model_validate(parsed_json)

        # Return as dict
        return validated_data.dict()

    except json.JSONDecodeError:
        return {"error": "AI did not return valid JSON", "raw_response": response_text}
    except Exception as e:
        return {"error": str(e)}
