import numpy as np
from model import NeuralNetwork


# 🔥 Normalize function (VERY IMPORTANT)
def normalize(X):
    X = X.astype(float)
    X[:, 0] /= 24
    X[:, 1] /= 60
    X[:, 2] /= 120
    X[:, 3] /= 15
    X[:, 4] /= 6
    return X


# 🔥 Temporary dataset (we will replace with DB later)
def get_data():
    X = np.array([
        [12, 10, 60, 5, 2],
        [18, 5, 80, 3, 4],
        [9, 0, 50, 7, 1],
        [15, 20, 70, 2, 3],
        [20, 15, 90, 4, 5],
    ])

    y = np.array([
        [8],
        [3],
        [10],
        [5],
        [4],
    ])

    return X, y


if __name__ == "__main__":
    # Load data
    X, y = get_data()

    # Normalize
    X = normalize(X)

    # Create model
    nn = NeuralNetwork(input_size=5, hidden_size=8, output_size=1, lr=0.01)

    # Train
    losses = nn.train(X, y, epochs=1000)

    # Test
    preds = nn.forward(X)

    print("Predictions:\n", preds)
    print("Actual:\n", y)