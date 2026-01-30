import joblib
# Model loader to ensure the model is loaded only once
class ModelSingleton:
    _model = None
    _scaler = None
    _encoder = None

    @classmethod
    def load(cls):
        if cls._model is None:
            cls._model = joblib.load("crop_model_pipeline.pkl")
            cls._scaler = joblib.load("scaler.pkl")
            cls._encoder = joblib.load("label_encoder.pkl")
        return cls._model, cls._scaler, cls._encoder
