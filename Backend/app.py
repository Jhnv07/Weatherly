from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

HTML_TEMPLATE = """
<!doctype html>
<title>Weather Dashboard</title>
<h1>Check Weather</h1>
<form method="post">
    <input type="text" name="city" placeholder="Enter city name">
    <input type="submit" value="Get Weather">
</form>
{% if weather %}
    <h2>Weather in {{ weather.city }}:</h2>
    <ul>
        <li>Temperature: {{ weather.temp }}°C</li>
        <li>Feels like: {{ weather.feels_like }}°C</li>
        <li>Description: {{ weather.description }}</li>
        <li>Humidity: {{ weather.humidity }}%</li>
        <li>Wind speed: {{ weather.wind_speed }} m/s</li>
    </ul>
{% elif error %}
    <p style="color:red;">{{ error }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        if request.is_json:
            city = request.get_json().get("city")
            json_mode = True
        else:
            city = request.form.get("city")
            json_mode = False   

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }

            if json_mode:
                return jsonify(weather)
            
        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                error = "City not found. Please check the name and try again."
            else:
                error = "HTTP error occurred."
        except requests.exceptions.RequestException:
            error = "Network error occurred."
    return render_template_string(HTML_TEMPLATE, weather=weather, error=error)

@app.route("/api", methods=["POST", "OPTIONS"])
def api_weather():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    city = data.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        return jsonify({"error": "OpenWeather API key not configured"}), 500

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather_desc = data["weather"][0]["description"].lower()
        weather_type = "Clear"
        if "rain" in weather_desc:
            weather_type = "Rain"
        elif "snow" in weather_desc:
            weather_type = "Snow"
        elif "cloud" in weather_desc:
            weather_type = "Cloudy"
        elif "thunder" in weather_desc:
            weather_type = "Thunderstorm"
        elif "clear" in weather_desc or "sun" in weather_desc:
            weather_type = "Clear"

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather_type": weather_type
        }
        return jsonify(weather_data)
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return jsonify({"error": "City not found. Please check the name and try again."}), 404
        else:
            return jsonify({"error": f"HTTP error occurred: {e}"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error occurred: {e}"}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
