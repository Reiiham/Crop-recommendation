from pydantic import BaseModel

class InputData(BaseModel):
    latitude: float
    longitude: float
    N: float
    P: float
    K: float
    ph: float
