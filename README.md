# TRAVEL-TECH-CRISIS-APP
# 🛡️ TravelTech - Tourist Crisis Navigator & Multi-Language Alert Portal

> **Lightweight, real-time crisis navigation and full UI/UX localization portal designed to protect tourists and travelers during extreme weather emergencies and natural disasters.**

---

## 🚨 Problem Statement
During extreme weather emergencies (such as flash floods, cyclones, or severe coastal storms), tourists frequently face critical barriers:
* **Information Asymmetry & Language Barriers**: Emergency broadcast alerts and local safety instructions are often posted only in regional languages, leaving foreign or non-local tourists stranded or confused.
* **Lack of Real-Time Spatial Awareness**: Travelers often do not know whether their exact geographical coordinates intersect with active hazard zones or low-lying flood regions.
* **Fragmented Emergency Infrastructure**: Finding operational relief centers, emergency shelters, or medical facilities nearby during a crisis involves searching through unverified sources.

---

## 💡 The Solution: TravelTech Crisis Navigator
**TravelTech** is an end-to-end web application built using **Streamlit**, **OpenWeatherMap API**, and a **custom Python spatial hazard detection engine**. It provides an instant, zero-friction, highly localized dashboard engineered specifically for disaster response management.

### Key Capabilities:
1. **Live Weather & Celsius Conversion**: Fetches real-time temperature, humidity, wind speeds, and meteorological descriptions via OpenWeatherMap, forced cleanly to Celsius (`&units=metric`).
2. **Dual-Layer Localization Architecture (10 Languages)**: 
   * **Static UI Localization**: Instant translation across buttons, sidebar controls, headers, and metrics for **English, Tamil, Hindi, Spanish, French, Telugu, and Kannada,Russian,Italian,Mandarian,Chinese**
   * **Dynamic Payload Translation**: Real-time hazard descriptions and emergency advisories translated on-the-fly using the `MyMemory` translation pipeline.
3. **Spatial Hazard Detection Engine**: Pure Python ray-casting/polygon geometry engine that instantly evaluates whether a user's latitude and longitude fall within active Red/Yellow hazard zones.
4. **Emergency Safe Haven Registry**: Integrated directory of nearby hospitals, relief shelters, and police precincts complete with live bed availability tracking, distance calculation, and direct Google Maps navigation links.
5. **Interactive Crisis Simulation & SOS**: Includes a coordinate simulator to test different GPS points (e.g., inside vs. outside flood zones) and an emergency SOS panic trigger.

---

## 🛠️ System Architecture & File Structure

```text
travel-tech-crisis-app/
│
├── app.py                     # Main Streamlit web app UI & event loop
├── data_manager.py            # Live OpenWeatherMap ingestion & GeoJSON spatial mock zones
├── translation_engine.py      # UI string dictionary (7 languages) & MyMemory API batch translation
├── state_and_performance.py   # Session state management, caching decorators, & location logic
└── requirements.txt           # Core Python dependencies
