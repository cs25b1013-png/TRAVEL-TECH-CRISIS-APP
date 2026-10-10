import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from translation_engine import SUPPORTED_LANGUAGES, get_ui_text
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
def disable_right_click_menu():
    """Injects JavaScript into the parent window to disable right-click context menus."""
    js_code = """
    <script>
    // Disable right-click context menu globally across the app
    const doc = window.parent.document;
    doc.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });
    </script>
    """
    components.html(js_code, height=0, width=0)

# Call this right after page config in app.py
disable_right_click_menu()
initialize_session_state()
current_lang_name = st.session_state.get("selected_language_name", "English")

# -------------------------------------------------------------------
# 2. Sidebar Controls (Language & Location Simulator)
# -------------------------------------------------------------------
with st.sidebar:
    st.title(get_ui_text("portal_title", current_lang_name))

    # Language Selector
    st.subheader(get_ui_text("select_lang", current_lang_name))
    lang_names = list(SUPPORTED_LANGUAGES.keys())
    
    if current_lang_name not in lang_names:
        current_lang_name = "English"
        st.session_state["selected_language_name"] = "English"

    selected_lang = st.selectbox(
        "Choose your preferred language:",
        options=lang_names,
        index=lang_names.index(current_lang_name),
        label_visibility="collapsed"
    )
    
    if selected_lang != st.session_state.get("selected_language_name"):
        update_app_language(selected_lang)
        st.rerun()

    st.divider()

    # Location Simulator Controls
    st.subheader(get_ui_text("location_sim", current_lang_name))
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
    st.caption(get_ui_text("quick_loc", current_lang_name))
    col_red, col_green = st.columns(2)
    if col_red.button(get_ui_text("flood_zone_btn", current_lang_name)):
        update_user_location(12.8350, 80.1300)
        st.rerun()
    if col_green.button(get_ui_text("safe_loc_btn", current_lang_name)):
        update_user_location(12.8000, 80.1000)
        st.rerun()

    st.divider()

    # SOS Panic Trigger
    sos_label = (
        get_ui_text("cancel_sos", current_lang_name)
        if st.session_state["sos_active"]
        else get_ui_text("trigger_sos", current_lang_name)
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
st.title(get_ui_text("nav_title", current_lang_name))

# Active SOS Banner
if st.session_state["sos_active"]:
    st.error(
        f"🚨 **EMERGENCY SOS ACTIVE:** Your coordinates have been flagged for priority assistance ({cur_lat:.4f}, {cur_lon:.4f}). Stay calm and proceed to the nearest shelter shown below."
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
m1.metric(get_ui_text("current_cond", current_lang_name), str(translated_weather.get("weather_main", "-")))

temp_val = translated_weather.get("temp")
m2.metric(
    get_ui_text("temperature", current_lang_name),
    f"{temp_val} °C" if temp_val is not None else "-",
)

m3.metric(
    get_ui_text("wind_speed", current_lang_name),
    f"{translated_weather.get('wind_speed', '-')} km/h"
    if translated_weather.get("wind_speed")
    else "-",
)
m4.metric(
    get_ui_text("active_hazards", current_lang_name), len(translated_hazards.get("active_hazards", []))
)

st.divider()

# Map and Shelters Layout using Native Streamlit Map
col_map, col_info = st.columns([2, 1])

with col_map:
    st.subheader(get_ui_text("live_map_title", current_lang_name))

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
    st.subheader(get_ui_text("nearest_havens", current_lang_name))

    if not shelters_df.empty:
        for idx, row in shelters_df.iterrows():
            with st.expander(
                f"📍 {row['name']} ({row['distance_km']} km)", expanded=(idx == 0)
            ):
                st.write(f"**Category:** {row['category']}")
                st.write(f"**Address:** {row['address']}")
                st.write(f"**Emergency Contact:** {row['phone']}")
                st.write(
                    f"**Capacity:** {row['capacity_available']} / {row['capacity_total']} beds available"
                )
                st.link_button(
                    get_ui_text("navigate_here", current_lang_name),
                    f"https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}",
                    use_container_width=True,
                )
    else:
        st.info("No open emergency shelters detected nearby.")

# -------------------------------------------------------------------
# 5. Active Hazards List Footer
# -------------------------------------------------------------------
st.divider()
st.subheader(get_ui_text("active_warnings", current_lang_name))
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
