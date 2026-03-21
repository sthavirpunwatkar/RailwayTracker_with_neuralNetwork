from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from model.model import NeuralNetwork
from db.database import SessionLocal
from db.models import Prediction, RailwayGate

from app.services.railway_api import get_train_status
from app.services.location import get_nearest_gates

app = FastAPI()

# Load model
nn = NeuralNetwork(7, 12, 1)
nn.load("model_weights.npz")


#  Input schema
class InputData(BaseModel):
    train_number: str
    time: float
    speed: float
    day: int
    lat: float
    lon: float


#  Normalize function (SAME as training)
def normalize(X):
    X = X.astype(float)

    X[:, 0] /= 24     # time
    X[:, 1] /= 60     # delay
    X[:, 2] /= 120    # speed
    X[:, 3] /= 25     # distance (updated)
    X[:, 4] /= 6      # day
    # X[:,5] is_peak → no change
    X[:, 6] /= 60     # travel_time

    return X


@app.post("/predict")
def predict(data: InputData):

    db = SessionLocal()

    #  1. Get nearest gates (LIST)
    gates = db.query(RailwayGate).all()
    nearest_gates = get_nearest_gates(data.lat, data.lon, gates, k=3)

    #  2. Get delay from API
    status = get_train_status(data.train_number)
    delay = status["delay"]

    print("API Delay:", delay)

    #  3. Feature engineering
    is_peak = 1 if (8 <= data.time <= 11 or 17 <= data.time <= 20) else 0

    results = []

    #  4. Loop through each gate
    for gate, distance in nearest_gates:

        print("Gate:", gate.name, "Distance:", distance)

        travel_time = (distance / data.speed) * 60 if data.speed > 0 else 0

        X = np.array([[
            data.time,
            delay,
            data.speed,
            distance,
            data.day,
            is_peak,
            travel_time
        ]])

        # Normalize
        X = normalize(X)

        # Predict
        pred = nn.forward(X)
        pred_value = float(pred[0][0])

        pred_value = max(0, min(60, pred_value))

        results.append({
            "gate": gate.name,
            "distance_km": distance,
            "closing_time": pred_value,
            "lat": gate.latitude,
            "lon": gate.longitude
        })

        #  Save each prediction
        new_entry = Prediction(
            time=data.time,
            delay=delay,
            speed=data.speed,
            distance=distance,
            day=data.day,
            prediction=pred_value
        )
        db.add(new_entry)

    #  commit ONCE
    db.commit()
    db.close()

    #  sort results
    results.sort(key=lambda x: x["closing_time"])

    return {
        "predictions": results,
        "best_gate": results[0]["gate"] if results else None
    }