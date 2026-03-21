from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from model.model import NeuralNetwork
from db.database import SessionLocal
from db.models import Prediction, RailwayGate

from app.services.railway_api import get_train_status
from app.services.location import find_nearest_gate

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

    #  1. Get nearest gate
    gates = db.query(RailwayGate).all()
    nearest_gate, distance = find_nearest_gate(data.lat, data.lon, gates)

    print(" Nearest Gate:", nearest_gate.name)
    print(" Distance:", distance)

    #  2. Get delay from API
    status = get_train_status(data.train_number)
    delay = status["delay"]

    print(" API Delay:", delay)

    #  3. Feature engineering
    is_peak = 1 if (8 <= data.time <= 11 or 17 <= data.time <= 20) else 0
    travel_time = (distance / data.speed) * 60 if data.speed > 0 else 0

    #  4. Build input
    X = np.array([[
        data.time,
        delay,
        data.speed,
        distance,
        data.day,
        is_peak,
        travel_time
    ]])

    print(" RAW INPUT:", X)

    #  5. Normalize
    X = normalize(X)

    print(" NORMALIZED INPUT:", X)

    #  6. Predict
    pred = nn.forward(X)
    pred_value = float(pred[0][0])

    # Clamp output
    pred_value = max(0, min(60, pred_value))

    #  7. Save to DB
    new_entry = Prediction(
        time=data.time,
        delay=delay,
        speed=data.speed,
        distance=distance,
        day=data.day,
        prediction=pred_value
    )

    gate_name = nearest_gate.name
    dist_val = distance
    db.add(new_entry)
    db.commit()
    db.close()

    return {
        "predicted_closing_time": pred_value,
        "nearest_gate": gate_name,
        "distance_km": dist_val,
        "delay_used": delay
    }