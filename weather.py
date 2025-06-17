from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Simulated device status
devices = {
    "fan": {"status": "off"},
    "light": {"status": "off"},
    "heater": {"status": "off"}
}

WEATHER_API_KEY ="663639ff8d065a8ecb8792762cc9e1da" 
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Home route (prevents 404 at root)
@app.route("/")
def home():
    return " Flask API is running! Try /weather/Srinagar or /devices"

#  Weather route
@app.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    params = {
        "q": f"{city},IN",  # ensures it's treated as Indian city
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        })
    else:
        return jsonify({"error": "City not found"}), 404

#  All devices
@app.route("/devices", methods=["GET"])
def get_devices():
    return jsonify(devices)

#  Update device status
@app.route("/devices/<device_id>", methods=["POST"])
def update_device(device_id):
    if device_id not in devices:
        return jsonify({"error": "Device not found"}), 404
    status = request.json.get("status")
    if status not in ["on", "off"]:
        return jsonify({"error": "Invalid status"}), 400
    devices[device_id]["status"] = status
    return jsonify({device_id: devices[device_id]})

# Auto control logic based on temperature
@app.route("/auto-control", methods=["GET"])
def auto_control():
    city = request.args.get("city", "Srinagar")
    params = {
        "q": f"{city},IN",
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        temp = response.json()["main"]["temp"]
        if temp > 30:
            devices["fan"]["status"] = "on"
            devices["heater"]["status"] = "off"
        elif temp < 15:
            devices["fan"]["status"] = "off"
            devices["heater"]["status"] = "on"
        else:
            devices["fan"]["status"] = "off"
            devices["heater"]["status"] = "off"
        return jsonify({
            "city": city,
            "temperature": temp,
            "devices": devices
        })
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500

#  Start Flask app
if __name__ == "__main__":
    app.run(debug=True)
