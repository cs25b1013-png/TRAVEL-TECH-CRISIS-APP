import math
import pandas as pd
import streamlit as st

# Import backend modules for data ingestion and translation
from data_manager import get_disaster_dashboard_data
from translation_engine import (
    SUPPORTED_LANGUAGES,
    translate_hazard_assessment,
    translate_weather_info,
)


# ===================================================================
# 1. Standalone Pure-Python Spatial Math Engine
# ===================================================================
def point_in_polygon(x: float, y: float, polygon_coords: list) -> bool:
    """Pure Python Ray-Casting algorithm to check if point (x, y) is inside polygon.

    x = longitude, y = latitude
    polygon_coords = list of [lon, lat] pairs defining the boundary
    """
    n = len(polygon_coords)
    inside = False

    p1x, p1y = polygon_coords[0]
    for i in range(n + 1):
        p2x, p2y = polygon_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def evaluate_user_hazard_status(
    user_lat: float, user_lon: float, hazards_geojson: dict
) -> dict:
    """Evaluates user hazard status using pure Python ray-casting math."""
    highest_risk = "GREEN"
    matched_hazards = []

    for feature in hazards_geojson.get("features", []):
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        if geometry.get("type") == "Polygon":
            coordinates = geometry.get("coordinates", [])[0]

            # Ray-casting check: user_lon is X, user_lat is Y
            if point_in_polygon(user_lon, user_lat, coordinates):
                risk_level = properties.get("risk_level", "YELLOW")
                matched_hazards.append({
                    "zone_id": properties.get("zone_id"),
                    "name": properties.get("name"),
                    "risk_level": risk_level,
                    "hazard_type": properties.get("hazard_type"),
                    "description_local": properties.get("description_local"),
                })

                if risk_level == "RED":
                    highest_risk = "RED"
                elif risk_level == "YELLOW" and highest_risk != "RED":
                    highest_risk = "YELLOW"

    status_messages = {
        "RED": "HIGH RISK: You are inside an active evacuation/hazard zone!",
        "YELLOW": (
            "WARNING: You are in a high-alert coastal or weather-affected"
            " zone."
        ),
        "GREEN": (
            "SAFE: No active geographic hazard boundaries detected at your"
            " location."
        ),
    }

    return {
        "status_code": highest_risk,
        "status_message": status_messages[highest_risk],
        "active_hazards": matched_hazards,
    }


def calculate_haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Calculates great-circle distance between two GPS points in kilometers."""
    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def find_nearest_safe_havens(
    user_lat: float,
    user_lon: float,
    safe_havens_df: pd.DataFrame,
    top_n: int = 3,
) -> pd.DataFrame:
    """Calculates distance to all operational safe havens and returns the top N nearest."""
    if safe_havens_df.empty:
        return pd.DataFrame()

    df = safe_havens_df.copy()

    df["distance_km"] = df.apply(
        lambda row: calculate_haversine_distance(
            user_lat, user_lon, row["lat"], row["lon"]
        ),
        axis=1,
    )

    open_shelters = df[df["is_open"] == True].sort_values(by="distance_km")
    return open_shelters.head(top_n)


def run_spatial_analysis(
    user_lat: float, user_lon: float, dashboard_data: dict
) -> dict:
    """Central spatial audit function combining hazard risk evaluation and nearest shelter calculations."""
    hazard_assessment = evaluate_user_hazard_status(
        user_lat, user_lon, dashboard_data["hazards_geojson"]
    )

    nearest_shelters = find_nearest_safe_havens(
        user_lat, user_lon, dashboard_data["safe_havens_df"]
    )

    return {
        "user_coordinates": {"lat": user_lat, "lon": user_lon},
        "hazard_assessment": hazard_assessment,
        "nearest_shelters": nearest_shelters,
    }


# ===================================================================
# 2. Cached Streamlit Performance Layer
# ===================================================================
@st.cache_data(ttl=1800, show_spinner="Fetching crisis & weather feeds...")
def load_cached_dashboard_data(lat: float, lon: float) -> dict:
    """Caches data ingestion pipeline (Weather API + GeoJSON + Safe Havens)."""
    return get_disaster_dashboard_data(lat, lon)


@st.cache_data(
    ttl=1800, show_spinner="Calculating hazard zones & nearby shelters..."
)
def load_cached_spatial_analysis(
    lat: float, lon: float, _dashboard_data: dict
) -> dict:
    """Caches point-in-polygon ray-casting checks and distance calculations.

    The leading underscore on `_dashboard_data` prevents Streamlit hashing errors on dicts.
    """
    return run_spatial_analysis(lat, lon, _dashboard_data)


@st.cache_data(
    ttl=3600, show_spinner="Translating alerts into native language..."
)
def load_cached_translated_hazard_assessment(
    hazard_assessment: dict, target_lang_code: str
) -> dict:
    """Caches batch translation outputs in memory to prevent rate limits."""
    return translate_hazard_assessment(hazard_assessment, target_lang_code)


@st.cache_data(ttl=3600)
def load_cached_translated_weather(
    weather_data: dict, target_lang_code: str
) -> dict:
    """Caches weather description translations."""
    return translate_weather_info(weather_data, target_lang_code)


# ===================================================================
# 3. Session State Management & Initializers
# ===================================================================
def initialize_session_state():
    """Initializes persistent global session variables.

    Call at the top of main Streamlit app.py.
    """
    if "user_lat" not in st.session_state:
        st.session_state["user_lat"] = 12.8350

    if "user_lon" not in st.session_state:
        st.session_state["user_lon"] = 80.1300

    if "selected_language_name" not in st.session_state:
        st.session_state["selected_language_name"] = "English"

    if "target_lang_code" not in st.session_state:
        st.session_state["target_lang_code"] = "en"

    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "Live Map"

    if "sos_active" not in st.session_state:
        st.session_state["sos_active"] = False


def update_user_location(new_lat: float, new_lon: float):
    """Updates GPS coordinates in session state."""
    st.session_state["user_lat"] = new_lat
    st.session_state["user_lon"] = new_lon


def update_app_language(lang_name: str):
    """Updates target translation language code in session state."""
    st.session_state["selected_language_name"] = lang_name
    st.session_state["target_lang_code"] = SUPPORTED_LANGUAGES.get(
        lang_name, "en"
    )


def toggle_sos_alert():
    """Toggles emergency SOS mode state."""
    st.session_state["sos_active"] = not st.session_state["sos_active"]


# ===================================================================
# 4. Streamlit Sidebar Controls Renderer
# ===================================================================
def render_sidebar_controls():
    """Renders Streamlit sidebar controls for language, location, and SOS status."""
    st.sidebar.header("⚙️ Dashboard Controls")

    # Language selection dropdown
    selected_lang = st.sidebar.selectbox(
        "Select Language / மொழி",
        options=list(SUPPORTED_LANGUAGES.keys()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(
            st.session_state.get("selected_language_name", "English")
        )
    )
    if selected_lang != st.session_state.get("selected_language_name"):
        update_app_language(selected_lang)
        st.rerun()

    st.sidebar.divider()

    # GPS Location Inputs
    st.sidebar.subheader("📍 GPS Location")
    lat = st.sidebar.number_input(
        "Latitude", value=float(st.session_state.get("user_lat", 12.8350)), format="%.4f"
    )
    lon = st.sidebar.number_input(
        "Longitude", value=float(st.session_state.get("user_lon", 80.1300)), format="%.4f"
    )

    if lat != st.session_state.get("user_lat") or lon != st.session_state.get("user_lon"):
        update_user_location(lat, lon)
        st.rerun()

    st.sidebar.divider()

    # Emergency SOS Toggle Button
    sos_active = st.session_state.get("sos_active", False)
    sos_label = "🚨 Emergency SOS Active" if sos_active else "⚠️ Trigger SOS"
    if st.sidebar.button(sos_label, type="primary" if not sos_active else "secondary", use_container_width=True):
        toggle_sos_alert()
        st.rerun()

    # Return the 3 values expected by app.py
    return (
        st.session_state.get("user_lat", 12.8350),
        st.session_state.get("user_lon", 80.1300),
        st.session_state.get("selected_language_name", "English")
    )


# ===================================================================
# Local Execution Test
# ===================================================================
if __name__ == "__main__":
    print(
        "=== STATE AND PERFORMANCE MODULE LOADED (STANDALONE SPATIAL ENGINE)"
        " ==="
    )
