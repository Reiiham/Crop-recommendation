from fastapi import APIRouter
from app.schemas.input_schema import InputData
from app.services.prediction_service import PredictionService

router = APIRouter()

@router.post("/predict")
def predict(data: InputData):
    crops, temp, humidity, rainfall, warnings = PredictionService.predict_crop(data)

    return {
    "recommended_crops": crops,
    "weather": {
        "temperature": temp,
        "humidity": humidity,
        "rainfall": rainfall
    },
    "warnings": warnings
}


