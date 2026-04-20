from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os
from app.logger import setup_logger

logger = setup_logger("liver_api", "INFO")

model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
if not os.path.exists(model_path):
     logger.critical("Model file not found {moedl_path}.")
     raise FileNotFoundError(f"Model file not found {model_path}.")

with open(model_path, "rb") as f:
     model = pickle.load(f)

logger.info(f"Model loaded.")

app = FastAPI(title="Liver Disease Prediction API", version="1.0.0")

class InputData(BaseModel):
    age: int
    gender: int
    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: int
    alamine_aminotransferase: int
    aspartate_aminotransferase: int
    total_proteins: float
    albumin: float
    albumin_and_globulin_ratio: float

@app.get("/")
def home():
     logger.info("Health check.")
     return {"status": "Api is running"}

@app.post("/predict")
def predict(data: InputData):
    features = [
        data.age, data.gender, data.total_bilirubin, data.direct_bilirubin,
        data.alkaline_phosphotase, data.alamine_aminotransferase,
        data.aspartate_aminotransferase, data.total_proteins,
        data.albumin, data.albumin_and_globulin_ratio
    ]
    try:
        prediction = model.predict([features])[0]
        logger.info(f"Prediction: {features} -> {prediction}")
        return {"prediction": float(prediction)}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}