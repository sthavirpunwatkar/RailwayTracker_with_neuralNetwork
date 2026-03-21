import streamlit as st
import requests

st.title("🚆 Railway Gate Prediction System")

# 🔹 Inputs
train_number = st.text_input("Train Number", "12051")
time = st.slider("Time (Hour)", 0, 23, 14)
speed = st.number_input("Train Speed (km/h)", min_value=1.0, value=60.0)

day = st.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
day_map = {
    "Mon": 0, "Tue": 1, "Wed": 2,
    "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6
}

# 🔹 Location
st.subheader("📍 Location")
lat = st.number_input("Latitude", value=18.5204)
lon = st.number_input("Longitude", value=73.8567)

# 🔹 Predict Button
if st.button("Predict"):

    url = "http://127.0.0.1:8000/predict"

    data = {
        "train_number": train_number,
        "time": time,
        "speed": speed,
        "day": day_map[day],
        "lat": lat,
        "lon": lon
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()

        st.success("✅ Prediction Successful")

        predictions = result.get("predictions", [])
        best_gate = result.get("best_gate")

        # 🔥 Highlight best gate
        if best_gate:
            st.markdown(f"### 🏆 Best Gate: **{best_gate}**")

        st.subheader("🚦 Gate Predictions")

        # 🔥 Display all gates
        for r in predictions:
            st.metric(
                label=f"🚆 {r['gate']}",
                value=f"{r['closing_time']:.2f} min",
                delta=f"{r['distance_km']:.2f} km"
            )

    else:
        st.error("❌ API Error")