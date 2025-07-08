import requests
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print("❌ City not found. Please check the name and try again.")
        else:
            print(f"❌ HTTP error occurred: {http_err}")
        return
    except requests.exceptions.RequestException as err:
        print(f"❌ Network error: {err}")
        return
    
    data = response.json()
    # Extract desired information
    city_name = data["name"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]
    
    # Display nicely
    print(f"\nWeather in {city_name}:")
    print(f"Temperature: {temp}°C")
    print(f"Description: {desc}")
    print(f"Humidity: {humidity}%")
    print(f"Wind speed: {wind_speed} m/s")


    # Append to a log file
    with open("weather_log.txt", "a", encoding="utf-8") as f:
        f.write(f"City: {city_name}\n")
        f.write(f"Temperature: {temp}°C (Feels like: {feels_like}°C)\n")
        f.write(f"Description: {desc}\n")
        f.write(f"Humidity: {humidity}%\n")
        f.write(f"Wind speed: {wind_speed} m/s\n")
        f.write("-" * 30 + "\n")

if __name__ == "__main__":
    city = input("Enter a city name: ")
    get_weather(city)

