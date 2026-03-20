import streamlit as st
import numpy as np
from model import NeuralNetwork

st.title("Neural Network From Scratch Demo")

# Inputs
x1 = st.slider("Feature 1", -2.0, 2.0, 0.0)
x2 = st.slider("Feature 2", -2.0, 2.0, 0.0)

# Dummy trained model
nn = NeuralNetwork(2, 10, 1)

# Fake training (quick demo)
X = np.random.randn(100, 2)
y = (X[:, 0] + X[:, 1] > 0).astype(int).reshape(-1, 1)
nn.train(X, y, epochs=200)

prediction = nn.forward(np.array([[x1, x2]]))

st.write("Prediction:", float(prediction.item()))