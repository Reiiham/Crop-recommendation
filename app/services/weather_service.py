import requests
from datetime import datetime

class WeatherService:

    @staticmethod
    def get_weather(latitude: float, longitude: float, month=None):
        if month is None:
            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={latitude}&longitude={longitude}"
                "&current_weather=true"
                "&hourly=relativehumidity_2m,precipitation"
            )

            try:
                response = requests.get(url, timeout=5)  # ⏱ max 5 sec
                data = response.json()

                temp = data["current_weather"]["temperature"]
                humidity = data["hourly"]["relativehumidity_2m"][0]
                rainfall = data["hourly"]["precipitation"][0]

                return temp, humidity, rainfall
            except Exception as e:
                print("Weather API error:", e)
                # Valeurs par défaut pour éviter que l'API bloque
                return 25, 60, 0
        else:
            url = (
            "https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={latitude}&longitude={longitude}"
            f"&start_date=2023-{month:02d}-01&end_date=2023-{month:02d}-28"
            "&daily=temperature_2m_mean,precipitation_sum"
            "&timezone=auto"
        )
            try:
                response = requests.get(url, timeout=5).json()  
                temps = response["daily"]["temperature_2m_mean"]
                rainfalls = response["daily"]["precipitation_sum"]
                avg_temp = sum(temps) / len(temps)
                total_rain = sum(rainfalls)
                humidity = 70  # Valeur par défaut approximative
                return avg_temp, humidity, total_rain

            except Exception as e:
                print("Weather API error:", e)
                # Valeurs par défaut pour éviter que l'API bloque
                return 25, 60, 0

