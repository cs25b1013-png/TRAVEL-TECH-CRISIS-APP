import json
import os
import pandas as pd
import requests

# -------------------------------------------------------------------
# Configuration & Constants
# -------------------------------------------------------------------
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "8212588a2a05ab6adc036c151d4db1c6")
DEFAULT_LAT = 12.8379  # Default coordinates (e.g., IIITDM Kancheepuram area)
DEFAULT_LON = 80.1373


# -------------------------------------------------------------------
# 1. Live Weather & Alert Fetching (Fahrenheit Units)
# -------------------------------------------------------------------
def fetch_live_weather_and_alerts(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """Fetches real-time weather parameters and weather alerts from OpenWeatherMap."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Chennai,in&units=imperial&APPID=8212588a2a05ab6adc036c151d4db1c6"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "temp": data.get("main", {}).get("temp"),
                "humidity": data.get("main", {}).get("humidity"),
                "weather_main": data.get("weather", [{}])[0].get("main", "Clear"),
                "description": data.get("weather", [{}])[0].get("description", "No active alerts"),
                "wind_speed": data.get("wind", {}).get("speed")
            }
    except Exception as e:
        print(f"[Warning] Weather API Request Failed: {e}")
    
    # Fallback response with temperature in Fahrenheit (83.3°F)
    return {
        "status": "fallback",
        "temp": 83.3,
        "humidity": 88,
        "weather_main": "Rain",
        "description": "Heavy rainfall warning issued for localized low-lying areas.",
        "wind_speed": 14.2
    }


# -------------------------------------------------------------------
# 2. Mock Hazard Zones (GeoJSON Fallback)
# -------------------------------------------------------------------
def get_mock_hazard_zones():
    """Returns GeoJSON spatial polygons representing active flood/disaster hazard zones."""
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "zone_id": "HZ_01",
                    "name": "Kancheepuram Low-Lying Flood Area",
                    "risk_level": "RED",
                    "hazard_type": "Flash Flood",
                    "description_local": "Severe waterlogging reported. Roads impassable for light vehicles."
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [80.1250, 12.8300],
                        [80.1450, 12.8300],
                        [80.1450, 12.8450],
                        [80.1250, 12.8450],
                        [80.1250, 12.8300]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "zone_id": "HZ_02",
                    "name": "Coastal Wind Warning Radius",
                    "risk_level": "YELLOW",
                    "hazard_type": "High Winds",
                    "description_local": "Strong coastal gusts. Avoid standing near weak structures or trees."
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [80.1450, 12.8200],
                        [80.1650, 12.8200],
                        [80.1650, 12.8550],
                        [80.1450, 12.8550],
                        [80.1450, 12.8200]
                    ]]
                }
            }
        ]
    }
    return geojson_data


# -------------------------------------------------------------------
# 3. Safe Haven & Emergency Infrastructure Registry
# -------------------------------------------------------------------
def load_safe_havens():
    """Loads structured registry of emergency shelters, hospitals, and police centers."""
    shelters_data = [
        {
            "shelter_id": "SH_101",
            "name": "Community Relief Center Kancheepuram",
            "category": "Emergency Shelter",
            "lat": 12.8500,
            "lon": 80.1200,
            "address": "45 Station Road, Ward 3",
            "phone": "+91 44 2722 0000",
            "capacity_total": 500,
            "capacity_available": 180,
            "is_open": True
        },
        {
            "shelter_id": "SH_102",
            "name": "District General Hospital",
            "category": "Medical Facility",
            "lat": 12.8350,
            "lon": 80.1150,
            "address": "Hospital Avenue, Main Circle",
            "phone": "+91 44 2722 1111",
            "capacity_total": 200,
            "capacity_available": 35,
            "is_open": True
        },
        {
            "shelter_id": "SH_103",
            "name": "Tourist Help & Police Precinct",
            "category": "Police & Tourist Assistance",
            "lat": 12.8420,
            "lon": 80.1550,
            "address": "ECR Main Crossing",
            "phone": "+91 44 2722 2222",
            "capacity_total": 50,
            "capacity_available": 20,
            "is_open": True
        }
    ]
    return pd.DataFrame(shelters_data)


# -------------------------------------------------------------------
# Hybrid Container (Supports Dict Lookup AND Unpacking)
# -------------------------------------------------------------------
class DashboardData(dict):
    """Allows dictionary-style access while supporting tuple unpacking (hazard_polygons, shelters)."""
    def __iter__(self):
        return iter((self.get("hazards_geojson"), self.get("safe_havens_df")))


# -------------------------------------------------------------------
# 4. Central Ingestion Entry Point
# -------------------------------------------------------------------
def get_disaster_dashboard_data(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """Central function to assemble all spatial, alert, and infrastructure data."""
    return DashboardData({
        "weather": fetch_live_weather_and_alerts(lat, lon),
        "hazards_geojson": get_mock_hazard_zones(),
        "safe_havens_df": load_safe_havens()
    })


# Testing execution
if __name__ == "__main__":
    data = get_disaster_dashboard_data()
    print("=== LIVE/FALLBACK WEATHER ===")
    print(data["weather"])
    print("\n=== ACTIVE HAZARD ZONES ===")
    print(f"Loaded {len(data['hazards_geojson']['features'])} hazard zones.")
    print("\n=== SAFE HAVENS REGISTERED ===")
    print(data["safe_havens_df"][["name", "category", "capacity_available"]])
