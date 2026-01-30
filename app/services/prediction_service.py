from json import encoder
from xml.parsers.expat import model
import pandas as pd
from app.models.model_loader import ModelSingleton
from app.services.weather_service import WeatherService

class PredictionService:

    @staticmethod
    def predict_crop(data):
        model, scaler, encoder = ModelSingleton.load()

        temp, humidity, rainfall = WeatherService.get_weather(
            data.latitude, data.longitude
        )

        # Toutes les valeurs possibles
        input_dict = {
    "N": data.N,
    "P": data.P,
    "K": data.K,
    "temperature": temp,
    "humidity": humidity,
    "ph": data.ph,
    "rainfall": rainfall
    }

# 🔥 Utilise EXACTEMENT le même ordre que pendant le training
        ordered_columns = scaler.feature_names_in_
        df = pd.DataFrame([[input_dict[col] for col in ordered_columns]],
                  columns=ordered_columns)

        scaled = scaler.transform(df)   
        pred = model.predict(scaled)
        crop =encoder.inverse_transform(pred)[0]

        return crop, temp, humidity, rainfall
