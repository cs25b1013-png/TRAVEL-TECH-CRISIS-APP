import pandas as pd
import streamlit as st

from translation_engine import SUPPORTED_LANGUAGES
# Import performance and state functions
from state_and_performance import (
    initialize_session_state,
    load_cached_dashboard_data,
    load_cached_spatial_analysis,
    load_cached_translated_hazard_assessment,
    load_cached_translated_weather,
    toggle_sos_alert,
    update_app_language,
    update_user_location,
)

# -------------------------------------------------------------------
# 1. Page Configuration & State Initialization
# -------------------------------------------------------------------
st.set_page_config(
    page_title="TravelTech - Tourist Crisis Navigator",
    page_icon="🚨",
    layout="wide",
)

initialize_session_state()

# -------------------------------------------------------------------
# 2. Sidebar Controls (Language & Location Simulator)
# -------------------------------------------------------------------
with st.sidebar:
    st.title("🛡️ Tourist Crisis Portal")

    # Language Selector (Safely handling SUPPORTED_LANGUAGES dictionary)
    st.subheader("🌐 Select Language")
    lang_names = list(SUPPORTED_LANGUAGES.keys())
    
    current_lang_name = st.session_state.get("selected_language_name", "English")
    if current_lang_name not in lang_names:
        current_lang_name = "English"
        st.session_state["selected_language_name"] = "English"

    selected_lang = st.selectbox(
        "Choose your preferred language:",
        options=lang_names,
        index=lang_names.index(current_lang_name),
    )
    
    if selected_lang != st.session_state.get("selected_language_name"):
        update_app_language(selected_lang)
        st.rerun()

    st.divider()

    # Location Simulator Controls
    st.subheader("📍 Location Simulator")
    sim_lat = st.number_input(
        "Latitude:",
        value=float(st.session_state["user_lat"]),
        format="%.4f",
        step=0.005,
    )
    sim_lon = st.number_input(
        "Longitude:",
        value=float(st.session_state["user_lon"]),
        format="%.4f",
        step=0.005,
    )

    if (
        sim_lat != st.session_state["user_lat"]
        or sim_lon != st.session_state["user_lon"]
    ):
        update_user_location(sim_lat, sim_lon)
        st.rerun()

    # Quick Preset Coordinates for Demo
    st.caption("Quick Test Locations:")
    col_red, col_green = st.columns(2)
    if col_red.button("🔴 Inside Flood Zone"):
        update_user_location(12.8350, 80.1300)
        st.rerun()
    if col_green.button("🟢 Safe Location"):
        update_user_location(12.8000, 80.1000)
        st.rerun()

    st.divider()

    # SOS Panic Trigger
    sos_label = (
        "🛑 CANCEL SOS"
        if st.session_state["sos_active"]
        else "🚨 TRIGGER EMERGENCY SOS"
    )
    if st.button(
        sos_label,
        use_container_width=True,
        type="primary" if not st.session_state["sos_active"] else "secondary",
    ):
        toggle_sos_alert()
        st.rerun()

# -------------------------------------------------------------------
# 3. Data Processing & Translations
# -------------------------------------------------------------------
cur_lat = st.session_state["user_lat"]
cur_lon = st.session_state["user_lon"]
lang_code = st.session_state["target_lang_code"]

# Fetch cached data & spatial evaluation
dashboard_data = load_cached_dashboard_data(cur_lat, cur_lon)
spatial_result = load_cached_spatial_analysis(cur_lat, cur_lon, dashboard_data)

# Fetch cached translations
translated_hazards = load_cached_translated_hazard_assessment(
    spatial_result["hazard_assessment"], lang_code
)
translated_weather = load_cached_translated_weather(
    dashboard_data["weather"], lang_code
)

# -------------------------------------------------------------------
# 4. Main UI Layout
# -------------------------------------------------------------------
st.title("🚨 Real-Time Tourist Safety Navigator")

# Active SOS Banner
if st.session_state["sos_active"]:
    st.error(
        "🚨 **EMERGENCY SOS ACTIVE:** Your coordinates have been flagged for"
        f" priority assistance ({cur_lat:.4f}, {cur_lon:.4f}). Stay calm and"
        " proceed to the nearest shelter shown below."
    )

# Risk Status Alert Banner
status_code = translated_hazards.get("status_code", "GREEN")
status_msg = translated_hazards.get("status_message", "")

if status_code == "RED":
    st.error(f"### {status_msg}")
elif status_code == "YELLOW":
    st.warning(f"### {status_msg}")
else:
    st.success(f"### {status_msg}")

# Live Metrics Bar
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Condition", str(translated_weather.get("weather_main", "-")))

temp_val = translated_weather.get("temp")
m2.metric(
    "Temperature",
    f"{temp_val} °C" if temp_val is not None else "-",
)

m3.metric(
    "Wind Speed",
    f"{translated_weather.get('wind_speed', '-')} km/h"
    if translated_weather.get("wind_speed")
    else "-",
)
m4.metric(
    "Active Hazard Zones", len(translated_hazards.get("active_hazards", []))
)

st.divider()

# Map and Shelters Layout using Native Streamlit Map
col_map, col_info = st.columns([2, 1])

with col_map:
    st.subheader("🗺️ Live Hazard Map & Shelter Locations")

    map_points = [
        {
            "latitude": cur_lat,
            "longitude": cur_lon,
            "color": "#FF0000" if status_code == "RED" else "#0000FF",
        }
    ]

    shelters_df = spatial_result["nearest_shelters"]
    if not shelters_df.empty:
        for _, row in shelters_df.iterrows():
            map_points.append(
                {"latitude": row["lat"], "longitude": row["lon"], "color": "#00FF00"}
            )

    map_df = pd.DataFrame(map_points)

    st.map(map_df, latitude="latitude", longitude="longitude", size=20, zoom=12)
    st.caption("🔴/🔵 Current Location | 🟢 Nearby Open Safe Havens")

with col_info:
    st.subheader("🏥 Nearest Safe Havens")

    if not shelters_df.empty:
        for idx, row in shelters_df.iterrows():
            with st.expander(
                f"📍 {row['name']} ({row['distance_km']} km)", expanded=(idx == 0)
            ):
                st.write(f"**Category:** {row['category']}")
                st.write(f"**Address:** {row['address']}")
                st.write(f"**Emergency Contact:** {row['phone']}")
                st.write(
                    f"**Capacity:** {row['capacity_available']} /"
                    f" {row['capacity_total']} beds available"
                )
                st.link_button(
                    "🗺️ Navigate Here",
                    f"https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}",
                    use_container_width=True,
                )
    else:
        st.info("No open emergency shelters detected nearby.")

# -------------------------------------------------------------------
# 5. Active Hazards List Footer
# -------------------------------------------------------------------
st.divider()
st.subheader("⚠️ Active Area Hazard Warnings")
active_list = translated_hazards.get("active_hazards", [])

if active_list:
    for item in active_list:
        st.warning(
            f"**{item.get('name')}** [{item.get('risk_level')} RISK]\n\n"
            f"**Hazard Type:** {item.get('hazard_type')}\n\n"
            f"**Details:** {item.get('description_local')}"
        )
else:
    st.info("No localized active hazard warnings found for your location.")
