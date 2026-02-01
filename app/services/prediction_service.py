from json import encoder
import warnings
from xml.parsers.expat import model
import pandas as pd
from app.models.model_loader import ModelSingleton
from app.services.weather_service import WeatherService
from datetime import datetime


# 🌍 Cultures compatibles Europe tempérée
EUROPE_COMPATIBLE_CROPS = {
    "maize", "grapes", "apple", "orange", "lentil", "chickpea", "rice"
}

# 🌡 Températures minimales réalistes
MIN_TEMP_REQUIREMENTS = {
    "maize": 10,
    "grapes": 10,
    "apple": 4,
    "orange": 12,
    "lentil": 5,
    "chickpea": 8,
    "rice": 15
}

# 📅 Calendrier simplifié Europe
EUROPE_CROP_CALENDAR = {
    "lentil": [3, 4],
    "chickpea": [3, 4],
    "maize": [4, 5, 6],
    "grapes": [2, 3, 4],
    "apple": [1, 2, 3],
    "orange": [3, 4],
    "rice": [4, 5]
}

class PredictionService:

    @staticmethod
    def predict_crop(data):
        model, scaler, encoder = ModelSingleton.load()

        # 🌦 Choisir météo selon mode
        if data.month and 1 <= data.month <= 12:
            temp, humidity, rainfall = WeatherService.get_weather(
                data.latitude, data.longitude, data.month
            )
            current_month = data.month
        else:
            temp, humidity, rainfall = WeatherService.get_weather(
                data.latitude, data.longitude
            )
            current_month = datetime.now().month

        # 📊 Préparer entrée modèle
        input_dict = {
            "N": data.N,
            "P": data.P,
            "K": data.K,
            "temperature": temp,
            "humidity": humidity,
            "ph": data.ph,
            "rainfall": rainfall
        }

        ordered_columns = scaler.feature_names_in_
        df = pd.DataFrame([[input_dict[col] for col in ordered_columns]],
                          columns=ordered_columns)

        scaled = scaler.transform(df)

        # 🔮 Probabilités modèle
        probs = model.predict_proba(scaled)[0]
        classes = encoder.inverse_transform(model.classes_)

        crop_probs = list(zip(classes, probs))
        crop_probs.sort(key=lambda x: x[1], reverse=True)

        top_crops = [
            {"crop": crop, "confidence": round(prob * 100, 2)}
            for crop, prob in crop_probs[:5]
        ]

        # 🌍 Filtrage Europe
        filtered_crops = [
            c for c in top_crops if c["crop"].lower() in EUROPE_COMPATIBLE_CROPS
        ]

        warnings = []

        if filtered_crops:
            final_crops = filtered_crops
        else:
            final_crops = [{"crop": "No suitable European crop found", "confidence": 0}]
            warnings.append("No crops from the European list match the current conditions.")

        # ⚠️ Vérifications climat
        for c in filtered_crops:
            crop_name = c["crop"].lower()

            # Température minimale
            min_temp = MIN_TEMP_REQUIREMENTS.get(crop_name)
            if min_temp and temp < min_temp:
                warnings.append(
                    f"{c['crop']} prefers temperatures above {min_temp}°C (current: {temp}°C)"
                )

            # Saison
            season_months = EUROPE_CROP_CALENDAR.get(crop_name)
            if season_months and current_month not in season_months:
                readable_months = ", ".join(str(m) for m in season_months)
                warnings.append(
                    f"{c['crop']} is usually planted in months [{readable_months}], current month is {current_month}"
                )

        return final_crops, temp, humidity, rainfall, warnings
