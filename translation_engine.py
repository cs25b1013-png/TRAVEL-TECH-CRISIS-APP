import requests
import streamlit as st

# Supported languages dictionary mapping name to code

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Telugu": "te",
    "Kannada": "kn"
}
UI_STRINGS = {
    "nav_title": {
        "en": "Real-Time Tourist Safety Navigator",
        "ta": "நிகழ்நேர சுற்றுலாப் பயணிகள் பாதுகாப்பு வழிகாட்டி",
        "hi": "रीयल-टाइम पर्यटक सुरक्षा नेविगेटर",
        "es": "Navegador de Seguridad Turística en Tiempo Real",
        "fr": "Navigateur de Sécurité Touristique en Temps Réel",
        "te": "నిజ-సమయ పర్యాటక భద్రతా నావిగేటర్",
        "kn": "ನೈಜ-ಸಮಯದ ಪ್ರವಾಸಿ ಸುರಕ್ಷತಾ ನ್ಯಾವಿಗೇಟರ್"
    },
    "portal_title": {
        "en": "🛡️ Tourist Crisis Portal",
        "ta": "🛡️ சுற்றுலாப் பயணிகள் நெருக்கடி மையம்",
        "hi": "🛡️ पर्यटक संकट पोर्टल",
        "es": "🛡️ Portal de Crisis Turística",
        "fr": "🛡️ Portail de Crise Touristique",
        "te": "🛡️ పర్యాటక సంక్షోభ పోర్టల్",
        "kn": "🛡️ ಪ್ರವಾಸಿ ಬಿಕ್ಕಟ್ಟು ಪೋರ್ಟಲ್"
    },
    "select_lang": {
        "en": "🌐 Select Language",
        "ta": "🌐 மொழியைத் தேர்ந்தெடுக்கவும்",
        "hi": "🌐 भाषा चुनें",
        "es": "🌐 Seleccionar Idioma",
        "fr": "🌐 Choisir la Langue",
        "te": "🌐 భాషను ఎంచుకోండి",
        "kn": "🌐 ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ"
    },
    "location_sim": {
        "en": "📍 Location Simulator",
        "ta": "📍 இருப்பிட சிமுலேட்டர்",
        "hi": "📍 स्थान सिम्युलेटर",
        "es": "📍 Simulador de Ubicación",
        "fr": "📍 Simulateur d'Emplacement",
        "te": "📍 స్థాన సిమ్యులేటర్",
        "kn": "📍 ಸ್ಥಳ ಸಿಮ್ಯುಲೇಟರ್"
    },
    "quick_loc": {
        "en": "Quick Test Locations:",
        "ta": "விரைவு சோதனை இடங்கள்:",
        "hi": "त्वरित परीक्षण स्थान:",
        "es": "Ubicaciones de Prueba Rápida:",
        "fr": "Emplacements de Test Rapide :",
        "te": "త్వరిత పరీక్ష స్థానాలు:",
        "kn": "ತ್ವರಿತ ಪರೀಕ್ಷಾ ಸ್ಥಳಗಳು:"
    },
    "flood_zone_btn": {
        "en": "🔴 Inside Flood Zone",
        "ta": "🔴 வெள்ளப் பகுதிக்குள்",
        "hi": "🔴 बाढ़ क्षेत्र के भीतर",
        "es": "🔴 Dentro de Zona de Inundación",
        "fr": "🔴 Dans la Zone Inondée",
        "te": "🔴 వరద ప్రాంతం లోపల",
        "kn": "🔴 ಪ್ರವಾಹ ಪ್ರದೇಶದ ಒಳಗೆ"
    },
    "safe_loc_btn": {
        "en": "🟢 Safe Location",
        "ta": "🟢 பாதுகாப்பான இடம்",
        "hi": "🟢 सुरक्षित स्थान",
        "es": "🟢 Ubicación Segura",
        "fr": "🟢 Emplacement Sûr",
        "te": "🟢 సురక్షిత ప్రాంతం",
        "kn": "🟢 ಸುರಕ್ಷಿತ ಸ್ಥಳ"
    },
    "cancel_sos": {
        "en": "🛑 CANCEL SOS",
        "ta": "🛑 SOS ஐ ரத்து செய்",
        "hi": "🛑 SOS रद्द करें",
        "es": "🛑 CANCELAR SOS",
        "fr": "🛑 ANNULER SOS",
        "te": "🛑 SOS రద్దు చేయండి",
        "kn": "🛑 SOS ರದ್ದುಗೊಳಿಸಿ"
    },
    "trigger_sos": {
        "en": "🚨 TRIGGER EMERGENCY SOS",
        "ta": "🚨 அவசர SOS ஐத் தூண்டவும்",
        "hi": "🚨 आपातकालीन SOS ट्रिगर करें",
        "es": "🚨 ACTIVAR SOS DE EMERGENCIA",
        "fr": "🚨 DÉCLENCHER SOS D'URGENCE",
        "te": "🚨 అత్యవసర SOSని ట్రిగర్ చేయండి",
        "kn": "🚨 ತುರ್ತು SOS ಅನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ"
    },
    "current_cond": {
        "en": "Current Condition",
        "ta": "தற்போதைய நிலை",
        "hi": "वर्तमान स्थिति",
        "es": "Condición Actual",
        "fr": "Condition Actuelle",
        "te": "ప్రస్తుత పరిస్థితి",
        "kn": "ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ"
    },
    "temperature": {
        "en": "Temperature",
        "ta": "வெப்பநிலை",
        "hi": "तापमान",
        "es": "Temperatura",
        "fr": "Température",
        "te": "ఉష్ణోగ్రత",
        "kn": "ತಾಪಮಾನ"
    },
    "wind_speed": {
        "en": "Wind Speed",
        "ta": "காற்றின் வேகம்",
        "hi": "हवा की गति",
        "es": "Velocidad del Viento",
        "fr": "Vitesse du Vent",
        "te": "గాలి వేగం",
        "kn": "ಗಾಳಿಯ ವೇಗ"
    },
    "active_hazards": {
        "en": "Active Hazard Zones",
        "ta": "செயலில் உள்ள ஆபத்து மண்டலங்கள்",
        "hi": "सक्रिय खतरे के क्षेत्र",
        "es": "Zonas de Peligro Activas",
        "fr": "Zones de Danger Actives",
        "te": "సక్రియ ప్రమాద ప్రాంతాలు",
        "kn": "ಸಕ್ರಿಯ ಅಪಾಯ ವಲಯಗಳು"
    },
    "live_map_title": {
        "en": "🗺️ Live Hazard Map & Shelter Locations",
        "ta": "🗺️ நேரலை ஆபத்து வரைபடம் & தங்குமிடங்கள்",
        "hi": "🗺️ लाइव खतरा मानचित्र और आश्रय स्थल",
        "es": "🗺️ Mapa de Peligros y Refugios en Vivo",
        "fr": "🗺️ Carte des Dangers et Refuges en Direct",
        "te": "🗺️ లై లైవ్ హజార్డ్ మ్యాప్ & ఆశ్రయ స్థానాలు",
        "kn": "🗺️ ಲೈವ್ ಅಪಾಯ ನಕ್ಷೆ ಮತ್ತು ಆಶ್ರಯ ಸ್ಥಳಗಳು"
    },
    "nearest_havens": {
        "en": "🏥 Nearest Safe Havens",
        "ta": "🏥 அருகிலுள்ள பாதுகாப்பான அடைக்கலங்கள்",
        "hi": "🏥 निकटतम सुरक्षित आश्रय",
        "es": "🏥 Refugios Seguros Más Cercanos",
        "fr": "🏥 Refuges Sûrs les Plus Proches",
        "te": "🏥 సమీప సురక్షిత ఆశ్రయాలు",
        "kn": "🏥 ಹತ್ತಿರದ ಸುರಕ್ಷಿತ ಆಶ್ರಯಗಳು"
    },
    "active_warnings": {
        "en": "⚠️ Active Area Hazard Warnings",
        "ta": "⚠️ செயலில் உள்ள பகுதி ஆபத்து எச்சரிக்கைகள்",
        "hi": "⚠️ सक्रिय क्षेत्र खतरा चेतावनियाँ",
        "es": "⚠️ Advertencias de Peligro en Área Activa",
        "fr": "⚠️ Avertissements de Danger en Zone Active",
        "te": "⚠️ సక్రియ ప్రాంత ప్రమాద హెచ్చరికలు",
        "kn": "⚠️ ಸಕ್ರಿಯ ಪ್ರದೇಶದ ಅಪಾಯದ ಎಚ್ಚರಿಕೆಗಳು"
    },
    "navigate_here": {
        "en": "🗺️ Navigate Here",
        "ta": "🗺️ இங்கு செல்லவும்",
        "hi": "🗺️ यहाँ नेविगेट करें",
        "es": "🗺️ Navegar Aquí",
        "fr": "🗺️ Naviguer Ici",
        "te": "🗺️ ఇక్కడకు నావిగేట్ చేయండి",
        "kn": "🗺️ ಇಲ್ಲಿಗೆ ನ್ಯಾವಿಗೇಟ್ ಮಾಡಿ"
    }
}

def get_ui_text(key: str, lang_name: str) -> str:
    """Retrieves localized UI text based on language name."""
    lang_code_map = {"English": "en", "Tamil": "ta", "Hindi": "hi", "Spanish": "es", "French": "fr", "Telugu": "te", "Kannada": "kn"}
    code = lang_code_map.get(lang_name, "en")
    
    if key in UI_STRINGS:
        return UI_STRINGS[key].get(code, UI_STRINGS[key].get("en", key))
    return key
# ===================================================================

def translate_text_batch(texts: list, target_language_code: str) -> list:
    """Translates a list of strings into the target language code using a public API."""
    if not target_language_code or target_language_code == "en":
        return texts

    translated_results = []
    for text in texts:
        if not text:
            translated_results.append("")
            continue
        try:
            url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(str(text))}&langpair=en|{target_language_code}"
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                translated_text = data.get("responseData", {}).get("translatedText", "")
                if translated_text and "MYMEMORY WARNING" not in translated_text:
                    translated_results.append(translated_text)
                    continue
        except Exception as e:
            print(f"[Warning] Translation API error: {e}")

        # Fallback tagging if API fails
        translated_results.append(f"[{target_language_code.upper()}] {text}")

    return translated_results


def translate_hazard_assessment(hazard_assessment: dict, target_lang_code: str) -> dict:
    """Translates hazard status messages and active hazards list."""
    if target_lang_code == "en":
        return hazard_assessment

    translated = hazard_assessment.copy()

    # Translate status message
    if "status_message" in translated:
        res = translate_text_batch([translated["status_message"]], target_lang_code)
        if res:
            translated["status_message"] = res[0]

    # Translate active hazards details
    active_hazards = []
    for hazard in translated.get("active_hazards", []):
        h_copy = hazard.copy()
        fields_to_translate = ["name", "description_local", "hazard_type"]
        texts_to_trans = [h_copy.get(f, "") for f in fields_to_translate]
        
        translated_texts = translate_text_batch(texts_to_trans, target_lang_code)
        
        for idx, field in enumerate(fields_to_translate):
            if idx < len(translated_texts):
                h_copy[field] = translated_texts[idx]
        active_hazards.append(h_copy)
        
    translated["active_hazards"] = active_hazards
    return translated


def translate_weather_info(weather_data: dict, target_lang_code: str) -> dict:
    """Translates weather description strings."""
    if target_lang_code == "en":
        return weather_data

    translated = weather_data.copy()
    fields = ["weather_main", "description"]
    texts = [translated.get(f, "") for f in fields]
    
    translated_texts = translate_text_batch(texts, target_lang_code)
    
    for idx, field in enumerate(fields):
        if idx < len(translated_texts):
            translated[field] = translated_texts[idx]
            
    return translated
