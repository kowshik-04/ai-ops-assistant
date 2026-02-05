import os
import requests
import time

class WeatherTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.max_retries = 3
        self.retry_delay = 1

    def get_weather(self, city: str):
        """Get current weather with retry logic"""
        if not self.api_key:
            raise Exception("OPENWEATHER_API_KEY not configured")
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                return {
                    "city": city,
                    "temperature_c": round(data["main"]["temp"], 1),
                    "feels_like_c": round(data["main"]["feels_like"], 1),
                    "humidity": data["main"]["humidity"],
                    "condition": data["weather"][0]["description"],
                    "wind_speed_ms": data["wind"]["speed"]
                }
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise Exception(f"Weather API error after {self.max_retries} retries: {str(e)}")
        
        return {}
