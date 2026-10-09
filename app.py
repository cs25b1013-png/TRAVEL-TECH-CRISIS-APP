import streamlit as st
from data_manager import fetch_live_weather_and_alerts, get_disaster_dashboard_data
from state_and_performance import initialize_session_state, render_sidebar_controls
from translation_engine import translate_batch_texts

# 1. Page Configuration
st.set_page_config(
    page_title="TravelTech Crisis Navigator",
    page_icon="🚨",
    layout="wide"
)

# 2. State Initialization
initialize_session_state()

# 3. Sidebar Controls
user_lat, user_lon, selected_lang = render_sidebar_controls()

# 4. Fetch Weather and Crisis Data
weather_info = fetch_live_weather_and_alerts(user_lat, user_lon)
hazard_polygons, shelters = get_disaster_dashboard_data()

# 5. Header Section
st.title("🚨 TravelTech Crisis Navigator")
st.caption("Real-time localized spatial safety & emergency response dashboard")

st.divider()

# 6. Primary Weather & Safety Metrics Display
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Temperature",
        value=f"{weather_info['temp']} °C"
    )

with col2:
    st.metric(
        label="Weather Condition",
        value=weather_info["weather_main"],
        delta=weather_info["description"]
    )

with col3:
    st.metric(
        label="Wind Speed",
        value=f"{weather_info['wind_speed']} km/h"
    )

st.divider()

# 7. Map & Spatial Engine Section
st.subheader("📍 Live Interactive Incident Map")

# Format shelter locations for st.map display
if shelters:
    map_data = [
        {"lat": s["lat"], "lon": s["lon"]} for s in shelters
    ] + [{"lat": user_lat, "lon": user_lon}]
    st.map(map_data)
else:
    st.map([{"lat": user_lat, "lon": user_lon}])

# 8. Emergency Status Summary
st.subheader("⚠️ Localized Weather Summary")
summary_text = (
    f"Current condition is {weather_info['weather_main']} ({weather_info['description']}) "
    f"with a temperature of {weather_info['temp']}°C and wind speed of {weather_info['wind_speed']} km/h."
)

if selected_lang != "English":
    translated_summary = translate_text_batch([summary_text], selected_lang)[0]
    st.info(translated_summary)
else:
    st.info(summary_text)
