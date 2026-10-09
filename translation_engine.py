from deep_translator import GoogleTranslator

# -------------------------------------------------------------------
# Supported Languages Configuration
# -------------------------------------------------------------------
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Spanish (Español)": "es",
    "French (Français)": "fr",
    "German (Deutsch)": "de",
    "Mandarin (中文)": "zh-CN",
    "Hindi (हिन्दी)": "hi",
    "Japanese (日本語)": "ja",
    "Arabic (العربية)": "ar"
}


# -------------------------------------------------------------------
# 1. Batch Translation Engine (Prevents Google 429 Rate Limits)
# -------------------------------------------------------------------
def translate_batch_texts(text_list: list, target_lang_code: str) -> list:
    """
    Translates a list of strings in a SINGLE HTTP request using batching
    to avoid Google rate limits.
    """
    if not text_list or target_lang_code == "en":
        return text_list

    # Filter out empty or non-string values while preserving indices
    non_empty_texts = [str(t) for t in text_list if t and str(t).strip()]
    if not non_empty_texts:
        return text_list

    try:
        translator = GoogleTranslator(source="auto", target=target_lang_code)
        translated_list = translator.translate_batch(non_empty_texts)

        result = []
        trans_idx = 0
        for original in text_list:
            if original and str(original).strip():
                result.append(translated_list[trans_idx])
                trans_idx += 1
            else:
                result.append(original)
        return result
    except Exception as e:
        print(f"[Warning] Batch translation failed: {e}")
        return text_list  # Safe fallback to original English text


# -------------------------------------------------------------------
# 2. Dynamic Hazard & Alert Translation
# -------------------------------------------------------------------
def translate_hazard_assessment(hazard_assessment: dict, target_lang_code: str) -> dict:
    """
    Translates status message and hazard details in a single batch call.
    """
    if target_lang_code == "en":
        return hazard_assessment

    translated_assessment = hazard_assessment.copy()
    hazards = hazard_assessment.get("active_hazards", [])

    # Collect all strings into one list
    to_translate = [hazard_assessment.get("status_message", "")]
    for h in hazards:
        to_translate.extend([
            h.get("name", ""),
            h.get("hazard_type", ""),
            h.get("description_local", "")
        ])

    # Execute single batch call
    translated_results = translate_batch_texts(to_translate, target_lang_code)

    # Re-assign translated values back
    translated_assessment["status_message"] = translated_results[0]

    idx = 1
    translated_hazards = []
    for h in hazards:
        translated_h = h.copy()
        translated_h["name"] = translated_results[idx]
        translated_h["hazard_type"] = translated_results[idx + 1]
        translated_h["description_local"] = translated_results[idx + 2]
        translated_hazards.append(translated_h)
        idx += 3

    translated_assessment["active_hazards"] = translated_hazards
    return translated_assessment


# -------------------------------------------------------------------
# 3. Dynamic Weather Broadcast Translation
# -------------------------------------------------------------------
def translate_weather_info(weather_data: dict, target_lang_code: str) -> dict:
    """
    Translates raw weather main condition and alert descriptions into target language.
    """
    if target_lang_code == "en":
        return weather_data

    translated_weather = weather_data.copy()
    to_translate = [
        weather_data.get("weather_main", ""),
        weather_data.get("description", "")
    ]

    translated_results = translate_batch_texts(to_translate, target_lang_code)

    translated_weather["weather_main"] = translated_results[0]
    translated_weather["description"] = translated_results[1]

    return translated_weather


# -------------------------------------------------------------------
# Execution & Testing Verification
# -------------------------------------------------------------------
if __name__ == "__main__":
    sample_weather = {
        "weather_main": "Rain",
        "description": "Heavy rainfall warning issued for localized low-lying areas."
    }
    
    print("=== TESTING TRANSLATION ENGINE MODULE ===")
    translated = translate_weather_info(sample_weather, "es")
    print("Spanish Weather Output:", translated)
