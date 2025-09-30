from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

sensor_data = {"temperature": 0, "humidity": 0}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify(sensor_data)

@app.route("/post_data", methods=["POST"])
def post_data():
    global sensor_data
    data = request.get_json()
    if data:
        sensor_data["temperature"] = data.get("temperature", 0)
        sensor_data["humidity"] = data.get("humidity", 0)
        return jsonify({"status": "success", "message": "Data received"}), 200
    return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
