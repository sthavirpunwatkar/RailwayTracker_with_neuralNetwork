import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Railway Gate Predictor", layout="centered")
st.title("🚆 Railway Gate AI Predictor")
st.markdown("### Predict gate closing time using real-time ML model")

st.divider()
st.write("Enter train details to predict gate closing time")

# Inputs
col1, col2 = st.columns(2)

with col1:
    time = st.slider("Time (Hour)", 0, 23, 12)
    train_number = st.text_input("Train Number", "12051")
    day = st.selectbox("Day of Week", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])

with col2:
    speed = st.number_input("Train Speed (km/h)", 1, 120, 60)
    distance = st.number_input("Distance to Gate (km)", 1, 20, 5)
if st.button("Predict"):

    day_map = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

    data = {
        "train_number": train_number,
        "time": time,
        "speed": speed,
        "distance": distance,
        "day": day_map[day]
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)

    if response.status_code == 200:
        pred = response.json()["predicted_closing_time"]

        st.metric(label="⏱️ Predicted Closing Time", value=f"{pred:.2f} min")
        st.info(f"🚆 Train Number Used: {train_number}")

        if pred > 30:
            st.warning("⚠️ Long wait expected")
        elif pred < 10:
            st.success("✅ Quick crossing expected")

if st.button("Show Recent Predictions"):
    res = requests.get("http://127.0.0.1:8000/last")
    data = res.json()

    st.write("### Recent Predictions")

    for row in data:
        st.write(row)



if st.button("Show Error Trend"):
    res = requests.get("http://127.0.0.1:8000/last")
    data = res.json()

    df = pd.DataFrame(data)

    if "error" in df:
        st.line_chart(df["error"])