from dataclasses import Field

from fastapi import FastAPI
import numpy as np
from model import NeuralNetwork
from pydantic import BaseModel
from Database.database import SessionLocal
from Database.models import Prediction

app = FastAPI()

class InputData(BaseModel):
    time: float
    delay: float
    speed: float = Field
    distance: float = Field
    day: int

def normalize(X):
    X = X.astype(float)
    X[:,0] /= 24
    X[:,1] /= 60
    X[:,2] /= 120
    X[:,3] /= 15
    X[:,4] /= 6
    return X

# load model once (important)
nn = NeuralNetwork(6, 8, 1)
nn.load("model_weights.npz")


@app.get("/")
def home():
    return {"message": "Railway NN API running"}


@app.post("/predict")
def predict(data: InputData):
    if data.speed <= 0 or data.distance <= 0:
        return {"error": "speed and distance must be > 0"}
    #new Feature
    is_peak = 1 if ( 8 <= data.time <=11 or 17 <= data.time <= 20 ) else 0
    X = np.array([[
        data.time,
        data.delay,
        data.speed,
        data.distance,
        data.day,
        is_peak
    ]])

    X = normalize(X)

    pred = nn.forward(X)
    pred_value = max( 0 , min(60, float(pred[0][0])))

    #store in db
    db = SessionLocal()

    record  = Prediction(
        time=data.time,
        delay=data.delay,
        speed=data.speed,
        distance=data.distance,
        day=data.day,
        prediction=pred_value)

    db.add(record)
    db.commit()
    db.close()
    return {"predicted_closing_time": pred_value}

@app.get("/last")
def last_predictions():
    db = SessionLocal()

    rows = db.query(Prediction).order_by(
        Prediction.id.desc()
    ).limit(5).all()

    db.close()

    return [
        {
            "prediction": r.prediction,
            "actual": r.actual_closing_time,
            "error": r.error
        }
        for r in rows
    ]