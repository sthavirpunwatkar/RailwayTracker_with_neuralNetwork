from fastapi import FastAPI
import numpy as np
from model import NeuralNetwork
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    time: float
    delay: float
    speed: float
    distance: float
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
nn = NeuralNetwork(5, 8, 1)
nn.load("model_weights.npz")


@app.get("/")
def home():
    return {"message": "Railway NN API running"}


@app.post("/predict")
def predict(data: InputData):
    X = np.array([[
        data.time,
        data.delay,
        data.speed,
        data.distance,
        data.day
    ]])

    X = normalize(X)

    pred = nn.forward(X)

    return {"predicted_closing_time": float(pred[0][0])}