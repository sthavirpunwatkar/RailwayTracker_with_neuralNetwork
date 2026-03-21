import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Railway Gate Predictor", layout="wide")

st.title("🚆 Railway Gate Prediction System")

# 🔥 Session state (VERY IMPORTANT)
if "result" not in st.session_state:
    st.session_state.result = None

# 🔹 Inputs
train_number = st.text_input("Train Number", "12051")

col1, col2 = st.columns(2)

with col1:
    time = st.slider("Time (Hour)", 0, 23, 14)
    speed = st.number_input("Train Speed (km/h)", min_value=1.0, value=60.0)

with col2:
    day = st.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    day_map = {
        "Mon": 0, "Tue": 1, "Wed": 2,
        "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6
    }

# 🔹 Location
st.subheader("📍 User Location")
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

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            st.session_state.result = response.json()
        else:
            st.error("❌ API Error")

    except Exception as e:
        st.error(f"Error: {str(e)}")


# 🔥 DISPLAY RESULTS (AFTER BUTTON)
result = st.session_state.result

if result:

    predictions = result.get("predictions", [])
    best_gate = result.get("best_gate")

    st.success("✅ Prediction Successful")

    # 🔥 Best Gate
    if best_gate:
        st.markdown(f"## 🏆 Best Gate: **{best_gate}**")

    st.subheader("🚦 Gate Predictions")

    # 🔥 Metrics
    cols = st.columns(len(predictions)) if predictions else []

    for i, r in enumerate(predictions):
        with cols[i]:
            st.metric(
                label=f"🚆 {r['gate']}",
                value=f"{r['closing_time']:.2f} min",
                delta=f"{r['distance_km']:.2f} km"
            )

    # 🔥 MAP (FOLIUM — STABLE)
    if predictions:

        st.subheader("🗺️ Map View")

        m = folium.Map(location=[lat, lon], zoom_start=12)

        # 🔵 User marker
        folium.Marker(
            [lat, lon],
            tooltip="User Location",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        # 🔴 Gate markers
        for r in predictions:
            if r.get("lat") and r.get("lon"):
                folium.Marker(
                    [r["lat"], r["lon"]],
                    tooltip=f"{r['gate']} ({r['closing_time']:.2f} min)",
                    icon=folium.Icon(color="red")
                ).add_to(m)

        st_folium(m, width=700, height=500)