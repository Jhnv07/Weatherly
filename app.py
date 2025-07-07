from flask import Flask, render_template_string, request
import requests

API_KEY = "887efcf80fa5f105904939a0f78540bb"

app = Flask(__name__)

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
        city = request.form.get("city")
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
        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                error = "City not found. Please check the name and try again."
            else:
                error = "HTTP error occurred."
        except requests.exceptions.RequestException:
            error = "Network error occurred."
    return render_template_string(HTML_TEMPLATE, weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
