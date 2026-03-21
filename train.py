import numpy as np
from model import NeuralNetwork
from Database.database import SessionLocal
from Database.models import Prediction


#  Normalize function (VERY IMPORTANT)
def normalize(X):
    X = X.astype(float)
    X[:, 0] /= 24
    X[:, 1] /= 60
    X[:, 2] /= 120
    X[:, 3] /= 15
    X[:, 4] /= 6
    X[:, 5] /= 1
    X[:, 6] /= 1
    # is_peak (index 5) → already 0 or 1 → no change needed
    return X

def load_from_db():
    db = SessionLocal()

    rows = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(100).all()
    db.close()

    X = []
    y = []

    for r in rows:
        if r.speed <= 0 or r.distance <= 0:
            continue

        if r.actual_closing_time is None :
            continue

        if not ( 0 <= r.actual_closing_time <= 60):
            continue

        if abs(r.error) > 20:
            continue

        is_peak = 1 if (8 <= r.time <= 11 or 17 <= r.time <= 20) else 0
        travel_time = r.distance / r.speed if r.speed > 0 else 0

        (X.append([
            r.time,
            r.delay,
            r.speed,
            r.distance,
            r.day,
            is_peak,
            travel_time
        ]))
        y.append([r.actual_closing_time])

    return np.array(X), np.array(y)

if __name__ == "__main__":
    # Load data
    X, y = load_from_db()
    if len(X) == 0:
        print("No Training Data Available")
        exit()
    print("Loaded samples:", len(X))
    print("Sample X:", X[:2])
    print("Sample y:", y[:2])

    # Normalize
    X = normalize(X)

    # Create model
    nn = NeuralNetwork(input_size=7, hidden_size=12, output_size=1, lr=0.01)

    # Train
    losses = nn.train(X, y, epochs=1000)
    nn.save("model_weights.npz")
    print("Model Saved")

    # Test
    preds = nn.forward(X)

    print("Predictions:\n", preds)
    print("Actual:\n", y)