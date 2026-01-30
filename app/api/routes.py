from fastapi import APIRouter
from app.schemas.input_schema import InputData
from app.services.prediction_service import PredictionService

router = APIRouter()

@router.post("/predict")
def predict(data: InputData):
    crop, temp, humidity, rainfall = PredictionService.predict_crop(data)

    return {
        "recommended_crop": crop,
        "weather": {
            "temperature": temp,
            "humidity": humidity,
            "rainfall": rainfall
        }
    }
