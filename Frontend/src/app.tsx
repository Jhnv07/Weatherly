import React, { useState } from 'react';
import { Search, MapPin, Thermometer, Droplets, Sun, Cloud, CloudRain, CloudSnow, Zap, Wind } from 'lucide-react';

interface WeatherData {
  city: string;
  temperature: number;
  description: string;
  humidity: number;
  weatherType: string;
}

function App() {
  const [city, setCity] = useState('');
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // Mock weather data for demonstration
  const mockWeatherData: WeatherData = {
    city: 'London',
    temperature: 22,
    description: 'Partly Cloudy',
    humidity: 65,
    weatherType: 'cloudy'
  };

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  if (!city.trim()) return;

  setIsLoading(true);
  setHasSearched(true);

  try {
    const response = await fetch("http://127.0.0.1:5000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ city: city.trim() }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch weather data');
    }

    setWeatherData({
      city: data.city,
      temperature: Math.round(data.temperature),
      description: data.description,
      humidity: data.humidity,
      weatherType: data.weather_type,
    });
  } catch (error) {
    console.error('Error fetching weather: ', error);
    setWeatherData(null);
  } finally {
    setIsLoading(false);
  }
};


  const getWeatherIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'sunny':
      case 'clear':
        return <Sun className="w-16 h-16 text-yellow-500" />;
      case 'cloudy':
      case 'partly cloudy':
        return <Cloud className="w-16 h-16 text-gray-500" />;
      case 'rainy':
      case 'rain':
        return <CloudRain className="w-16 h-16 text-blue-500" />;
      case 'snowy':
      case 'snow':
        return <CloudSnow className="w-16 h-16 text-blue-200" />;
      case 'stormy':
      case 'thunderstorm':
        return <Zap className="w-16 h-16 text-purple-500" />;
      default:
        return <Cloud className="w-16 h-16 text-gray-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-weather-bg to-weather-secondary/30 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12 animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Wind className="w-8 h-8 text-weather-primary" />
            <h1 className="text-4xl md:text-5xl font-bold text-weather-text">
              Weather Dashboard
            </h1>
          </div>
          <p className="text-weather-text/70 text-lg">
            Get real-time weather information for any city
          </p>
        </header>

        {/* Search Form */}
        <form 
          onSubmit={handleSubmit} 
          className="mb-12 animate-slide-up"
          id="weather-search-form"
        >
          <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-6 md:p-8">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <MapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-weather-text/40" />
                <input
                  type="text"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="Enter city name..."
                  className="w-full pl-12 pr-4 py-4 text-lg bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-weather-primary focus:border-transparent transition-all duration-200 text-weather-text placeholder-weather-text/50"
                  id="city-input"
                />
              </div>
              <button
                type="submit"
                disabled={isLoading || !city.trim()}
                className="px-8 py-4 bg-weather-primary text-white font-semibold rounded-xl hover:bg-weather-primary/90 focus:outline-none focus:ring-2 focus:ring-weather-primary/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg"
                id="get-weather-btn"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Loading...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    Get Weather
                  </>
                )}
              </button>
            </div>
          </div>
        </form>

        {/* Weather Display */}
        {hasSearched && (
          <div className="animate-slide-up" id="weather-display">
            {weatherData ? (
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-6 md:p-8">
                <div className="grid md:grid-cols-2 gap-8">
                  {/* Left Column - Main Weather Info */}
                  <div className="text-center md:text-left">
                    <div className="flex items-center justify-center md:justify-start gap-3 mb-4">
                      <MapPin className="w-6 h-6 text-weather-primary" />
                      <h2 className="text-2xl md:text-3xl font-bold text-weather-text" id="city-name">
                        {weatherData.city}
                      </h2>
                    </div>
                    
                    <div className="flex items-center justify-center md:justify-start gap-4 mb-6">
                      <div className="animate-pulse-slow" id="weather-icon">
                        {getWeatherIcon(weatherData.weatherType)}
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <Thermometer className="w-5 h-5 text-weather-primary" />
                          <span className="text-4xl md:text-5xl font-bold text-weather-text" id="temperature">
                            {weatherData.temperature}°C
                          </span>
                        </div>
                        <p className="text-weather-text/70 text-lg" id="weather-description">
                          {weatherData.description}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Right Column - Additional Details */}
                  <div className="space-y-6">
                    <div className="bg-weather-bg/50 rounded-xl p-4">
                      <div className="flex items-center gap-3 mb-2">
                        <Droplets className="w-5 h-5 text-weather-primary" />
                        <span className="text-weather-text/70 font-medium">Humidity</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-2xl font-bold text-weather-text" id="humidity">
                          {weatherData.humidity}%
                        </span>
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-weather-primary h-2 rounded-full transition-all duration-500"
                            style={{ width: `${weatherData.humidity}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-weather-secondary/20 rounded-xl p-4">
                      <div className="text-center">
                        <p className="text-weather-text/70 text-sm mb-1">Weather Status</p>
                        <p className="text-weather-text font-semibold text-lg capitalize" id="weather-status">
                          {weatherData.weatherType}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-12 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-weather-primary mx-auto mb-4"></div>
                <p className="text-weather-text/70 text-lg">Fetching weather data...</p>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <footer className="mt-16 text-center text-weather-text/50 text-sm">
          <p>Weather Dashboard - Real-time weather information at your fingertips</p>
        </footer>
      </div>
    </div>
  );
}

export default App;