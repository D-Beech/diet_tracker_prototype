from flask import Flask, render_template, request, jsonify
from services.ai_service import do_ai
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/api/voice", methods=["POST"])
def echo():
    data = request.get_json()
    do_ai(data)
    return jsonify({"you_sent": data})

if __name__ == "__main__":
    app.run(debug=True)
