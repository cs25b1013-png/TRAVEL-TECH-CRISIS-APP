import requests
import streamlit as st

# Comprehensive language code mapping for fallback translation
LANGUAGE_CODES = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Telugu": "te",
    "Kannada": "kn"
}

def translate_text_batch(texts: list, target_language: str) -> list:
    """
    Translates a list of strings into the target language.
    Falls back gracefully if the translation API is unreachable.
    """
    if target_language == "English" or not target_language:
        return texts

    target_code = LANGUAGE_CODES.get(target_language, "en")
    translated_results = []

    for text in texts:
        try:
            # Using a free public translation endpoint (MyMemory Translated API)
            url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(text)}&langpair=en|{target_code}"
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                translated_text = data.get("responseData", {}).get("translatedText", "")
                if translated_text and "MYMEMORY WARNING" not in translated_text:
                    translated_results.append(translated_text)
                    continue
        except Exception as e:
            print(f"[Warning] Translation API failed: {e}")

        # Fallback dictionary for common crisis terms if network/API fails
        fallback_map = {
            "Tamil": f"[তামিল / Ta] {text}",
            "Hindi": f"[हिंदी / Hi] {text}",
            "Spanish": f"[Español / Es] {text}",
            "French": f"[Français / Fr] {text}",
            "Telugu": f"[తెలుగు / Te] {text}",
            "Kannada": f"[ಕನ್ನಡ / Kn] {text}"
        }
        translated_results.append(fallback_map.get(target_language, text))

    return translated_results
