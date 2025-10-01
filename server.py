from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # <-- Import CORS

app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all routes

sensor_data = {"temperature": -1, "humidity": -1, "AQI": -1}
toggle = 0
manual_toggle = 0
threshold = 0

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify(sensor_data)

@app.route("/post_data", methods=["POST"])
def post_data():
    global sensor_data, toggle
    data = request.get_json()
    if data:
        sensor_data["temperature"] = data.get("temperature", 0)
        sensor_data["humidity"] = data.get("humidity", 0)
        sensor_data["AQI"] = data.get("AQI", 0)

        if manual_toggle == 0:
            toggle = 1 if sensor_data["temperature"] > threshold else 0

        return jsonify({
            "status": "success",
            "message": "Data received",
            "toggle": toggle
        }), 200

    return jsonify({"status": "error", "message": "No data received"}), 400

@app.route("/manual_toggle", methods=["POST"])
def manual_toggle_action():
    global manual_toggle, toggle
    manual_toggle = 1 - manual_toggle
    if manual_toggle == 1:
        toggle = 1
    return jsonify({
        "status": "success",
        "message": "Manual toggle state changed",
        "manual_toggle": manual_toggle,
        "toggle": toggle
    }), 200

@app.route("/set_threshold", methods=["POST"])
def set_threshold():    
    global threshold
    data = request.get_json()
    
    if data and "threshold" in data:
        threshold = float(data["threshold"])  # Convert to float
        global toggle
        if sensor_data["temperature"] != -1 and sensor_data["temperature"] > threshold and manual_toggle == 0:
            toggle = 1
        else:
            toggle = 0

        return jsonify({
            "status": "success",
            "message": "Threshold updated",
            "threshold": threshold
        }), 200
    return jsonify({"status": "error", "message": "No threshold provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
