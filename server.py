from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # For cross-origin access from frontend or ESP32

app = Flask(__name__)
CORS(app)

# Store sensor readings and control states
sensor_data = {"temperature": -1, "humidity": -1, "AQI": -1}
toggle = 0
threshold = 0

@app.route("/")
def index():
    return render_template("home.html")

# Get the latest sensor readings
@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify(sensor_data)

# Receive sensor readings from ESP32
@app.route("/post_data", methods=["POST"])
def post_data():
    global sensor_data, toggle, threshold
    data = request.get_json()

    if data:
        # Update sensor data
        sensor_data["temperature"] = data.get("temperature", 0)
        sensor_data["humidity"] = data.get("humidity", 0)
        sensor_data["AQI"] = data.get("AQI", 0)

        # Fan control logic
        if threshold == -1:
            toggle = 1  # Always ON
        elif threshold == 100:
            toggle = 0  # Always OFF
        else:
            toggle = 1 if sensor_data["temperature"] > threshold else 0

        return jsonify({
            "status": "success",
            "message": "Data received",
            "toggle": toggle
        }), 200

    return jsonify({"status": "error", "message": "No data received"}), 400


# Set temperature threshold or special values (-1 = always on, 100 = always off)
@app.route("/set_threshold", methods=["POST"])
def set_threshold():
    global threshold, toggle
    data = request.get_json()

    if data and "threshold" in data:
        threshold = float(data["threshold"])

        # Update toggle immediately when threshold changes
        if threshold == -1:
            toggle = 1
        elif threshold == 100:
            toggle = 0
        elif sensor_data["temperature"] != -1:
            toggle = 1 if sensor_data["temperature"] > threshold else 0
        else:
            toggle = 0

        return jsonify({
            "status": "success",
            "message": "Threshold updated",
            "threshold": threshold,
            "toggle": toggle
        }), 200

    return jsonify({"status": "error", "message": "No threshold provided"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
