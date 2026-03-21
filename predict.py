import numpy as np
from model import NeuralNetwork
import pickle

# same normalize function
def normalize(X):
    X = X.astype(float)
    X[:,0] /= 24
    X[:,1] /= 60
    X[:,2] /= 120
    X[:,3] /= 15
    X[:,4] /= 6
    return X


# create model (same shape as training)
nn = NeuralNetwork(7, 12, 1)

# load trained weights
nn.load("model_weights.npz")

# sample input
X_input = np.array([[14, 10, 60, 5, 2]])

X = normalize(X_input)

prediction = nn.forward(X)

print("Predicted closing time:", prediction[0][0])