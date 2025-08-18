from flask import Flask, request, jsonify
from services.ai_service import do_ai
from services.models import LogEntry
import os
from dotenv import load_dotenv


# Initialize Flask app
app = Flask(__name__)

# # Load Postgres credentials from environment
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", 5432)
# DB_NAME = os.getenv("DB_NAME")

# # Determine DATABASE_URL
# if DB_USER and DB_PASSWORD and DB_NAME:
#     # Use Postgres if credentials are provided
#     DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# else:
#     # Fallback to local SQLite for development
#     DATABASE_URL = "sqlite:///./app.db"

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Hello, Flask!"

def is_empty_log(entry: LogEntry) -> bool:
    """Check if the AI returned no useful data."""
    return (
        (entry.body_weight_kg is None) and
        (not entry.exercise) and
        (not entry.food)
    )


@app.route("/api/voice", methods=["POST"])
def process_voice():
    data = request.get_json()
    prompt = data.get("prompt", "")
    #time_stamp = data.get("time_stamp", None)

    # Call AI service
    ai_response = do_ai(prompt, openai_api_key)

    # If AI returned an error
    if "error" in ai_response:
        return jsonify({"status": "error", "message": ai_response["error"]}), 400

    # Parse into Pydantic model
    try:
        log_entry = LogEntry.model_validate(ai_response)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    # Check if AI returned nothing useful
    if is_empty_log(log_entry):
        return jsonify({
            "status": "empty",
            "message": "No useful data extracted from prompt",
            "data": log_entry.dict()
        }), 200

    return jsonify({
        "status": "success",
        "message": "Data extracted successfully",
        "data": log_entry.dict()
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
