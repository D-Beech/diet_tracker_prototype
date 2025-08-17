from flask import Flask, request, jsonify
from services.ai_service import do_ai
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/api/voice", methods=["POST"])
def voice():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Call AI service
    ai_response = do_ai(prompt, openai_api_key)
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
