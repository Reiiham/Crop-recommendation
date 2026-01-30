import requests

class WeatherService:

    @staticmethod
    def get_weather(latitude: float, longitude: float):
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

