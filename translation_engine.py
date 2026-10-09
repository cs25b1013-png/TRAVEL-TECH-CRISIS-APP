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
