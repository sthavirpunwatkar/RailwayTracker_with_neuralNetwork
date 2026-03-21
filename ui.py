import streamlit as st
import requests

st.set_page_config(page_title="Railway Gate Predictor", layout="centered")

st.title("🚆 Railway Gate Closing Time Predictor")

st.write("Enter train details to predict gate closing time")

# Inputs
time = st.slider("Time (Hour)", 0, 23, 12)
delay = st.number_input("Delay (minutes)", 0, 60, 5)
speed = st.number_input("Train Speed (km/h)", 1, 120, 60)
distance = st.number_input("Distance to Gate (km)", 1, 20, 5)
day = st.selectbox("Day of Week (0=Mon, 6=Sun)", list(range(7)))

# Predict button
if st.button("Predict"):

    data = {
        "time": time,
        "delay": delay,
        "speed": speed,
        "distance": distance,
        "day": day
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=data)

        if response.status_code == 200:
            result = response.json()
            pred = result["predicted_closing_time"]

            st.success(f"⏱️ Estimated Closing Time: {pred:.2f} minutes")

        else:
            st.error("API error")

    except:
        st.error("Could not connect to API. Is FastAPI running?")