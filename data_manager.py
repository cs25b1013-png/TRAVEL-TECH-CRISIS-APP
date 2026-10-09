import os
import requests
import pandas as pd
import streamlit as st

def get_weather_data(lat: float, lon: float, api_key: str = None) -> dict:
    """Fetches weather data using OpenWeatherMap API or falls back to mock data."""
    if not api_key:
        api_key = st.secrets.get("OPENWEATHER_API_KEY", None)

    if api_key:
        try:
            # Added &units=metric to force Celsius from the API
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                
                # Check and convert Kelvin to Celsius if API ignores units parameter
                temp_val = data["main"]["temp"]
                if temp_val > 100:  # If temp is in Kelvin
                    temp_val = temp_val - 273.15

                return {
                    "weather_main": data["weather"][0]["main"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "temp": round(temp_val, 1),
                    "wind_speed": round(data["wind"]["speed"] * 3.6, 1),
                }
        except Exception as e:
            print(f"[Warning] Weather API call failed, falling back to mock: {e}")

    # Fallback Mock Data
    return {
        "weather_main": "Rain / Storm",
        "description": "Heavy localized monsoon downpour with risk of flash waterlogging.",
        "temp": 28.5,
        "wind_speed": 42.0,
    }
