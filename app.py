from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify({"you_sent": data})

if __name__ == "__main__":
    app.run(debug=True)
