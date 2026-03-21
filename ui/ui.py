import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Railway Gate Predictor", layout="wide")

st.title("🚆 Railway Gate Prediction System")

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
            result = response.json()

            st.success("✅ Prediction Successful")

            predictions = result.get("predictions", [])
            best_gate = result.get("best_gate")

            # 🔥 Best Gate Highlight
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

            # 🔥 MAP (pydeck)
            if predictions:

                map_data = []

                # user location
                map_data.append({
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "type": "User"
                })

                # gate locations
                for r in predictions:
                    if r.get("lat") is not None and r.get("lon") is not None:
                        map_data.append({
                            "latitude": float(r["lat"]),
                            "longitude": float(r["lon"]),
                            "type": r["gate"]
                        })

                df = pd.DataFrame(map_data)

                st.subheader("🗺️ Map View")

                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position='[longitude, latitude]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                )

                view_state = pdk.ViewState(
                    latitude=df["latitude"].mean(),
                    longitude=df["longitude"].mean(),
                    zoom=12,
                    pitch=0,
                )

                deck = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                )

                st.pydeck_chart(deck)

        else:
            st.error("❌ API Error")

    except Exception as e:
        st.error(f"Error: {str(e)}")