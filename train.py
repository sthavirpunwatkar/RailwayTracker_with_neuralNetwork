import numpy as np
from model import NeuralNetwork
from Database.database import SessionLocal
from Database.models import Prediction


# 🔥 Normalize function (VERY IMPORTANT)
def normalize(X):
    X = X.astype(float)
    X[:, 0] /= 24
    X[:, 1] /= 60
    X[:, 2] /= 120
    X[:, 3] /= 15
    X[:, 4] /= 6
    return X


# # 🔥 Temporary dataset (we will replace with DB later)
# def get_data():
#     X = np.array([
#         [12, 10, 60, 5, 2],
#         [18, 5, 80, 3, 4],
#         [9, 0, 50, 7, 1],
#         [15, 20, 70, 2, 3],
#         [20, 15, 90, 4, 5],
#     ])
#
#     y = np.array([
#         [8],
#         [3],
#         [10],
#         [5],
#         [4],
#     ])
#
#     return X, y

def load_from_db():
    db = SessionLocal()

    rows = db.query(Prediction).filter(Prediction.actual_closing_time != None).all()
    db.close()

    X = []
    y = []

    for r in rows:
        X.append([r.time, r.delay, r.speed, r.distance, r.day])
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
    nn = NeuralNetwork(input_size=5, hidden_size=8, output_size=1, lr=0.01)

    # Train
    losses = nn.train(X, y, epochs=1000)
    nn.save("model_weights.npz")
    print("Model Saved")
    
    # Test
    preds = nn.forward(X)

    print("Predictions:\n", preds)
    print("Actual:\n", y)