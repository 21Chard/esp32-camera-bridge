from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "ESP32 Camera Bridge OK"

print("Starting Flask...")

app.run(host="0.0.0.0", port=8088, debug=True)
