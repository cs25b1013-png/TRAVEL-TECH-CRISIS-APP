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
    "Kannada": "kn",
    "German": "de",
    "Japanese": "ja",
    "Mandarin": "zh",
    "Italian": "it",
    "Russian": "ru",
    "Arabic": "ar"
    
}
UI_STRINGS = {
    "nav_title": {
        "en": "Real-Time Tourist Safety Navigator",
        "ta": "நிகழ்நேர சுற்றுலாப் பயணிகள் பாதுகாப்பு வழிகாட்டி",
        "hi": "रीयल-टाइम पर्यटक सुरक्षा नेविगेटर",
        "es": "Navegador de Seguridad Turística en Tiempo Real",
        "fr": "Navigateur de Sécurité Touristique en Temps Réel",
        "te": "నిజ-సమయ పర్యాటక భద్రతా నావిగేటర్",
        "kn": "ನೈಜ-ಸಮಯದ ಪ್ರವಾಸಿ ಸುರಕ್ಷತಾ ನ್ಯಾವಿಗೇಟರ್",
        "de": "Echtzeit-Tourismussicherheits-Navigator",
        "ja": "リアルタイム観光客安全ナビゲーター",
        "zh": "实时游客安全导航仪",
        "it": "Navigatore di Sicurezza Turistica in Tempo Reale",
        "ru": "Навигатор туристической безопасности в реальном времени",
        "ar": "متصفح أسلامي لسياحة الأمن الفوري"
    },
    "portal_title": {
        "en": "🛡️ Tourist Crisis Portal",
        "ta": "🛡️ சுற்றுலாப் பயணிகள் நெருக்கடி மையம்",
        "hi": "🛡️ पर्यटक संकट पोर्टल",
        "es": "🛡️ Portal de Crisis Turística",
        "fr": "🛡️ Portail de Crise Touristique",
        "te": "🛡️ పర్యాటక సంక్షోభ పోర్టల్",
        "kn": "🛡️ ಪ್ರವಾಸಿ ಬಿಕ್ಕಟ್ಟು ಪೋರ್ಟಲ್",
        "de": "🛡️ Touristen-Krisenportal",
        "ja": "🛡️ 観光客危機ポータル",
        "zh": "🛡️ 游客危机门户",
        "it": "🛡️ Portale Crisi Turistica",
        "ru": "🛡️ Портал туристических кризисов",
        "ar": "🛡️ بوابة الأزمات السياحية"
    },
    "select_lang": {
        "en": "🌐 Select Language",
        "ta": "🌐 மொழியைத் தேர்ந்தெடுக்கவும்",
        "hi": "🌐 भाषा चुनें",
        "es": "🌐 Seleccionar Idioma",
        "fr": "🌐 Choisir la Langue",
        "te": "🌐 భాషను ఎంచుకోండి",
        "kn": "🌐 ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "de": "🌐 Sprache auswählen",
        "ja": "🌐 言語を選択",
        "zh": "🌐 选择语言",
        "it": "🌐 Seleziona Lingua",
        "ru": "🌐 Выберите язык",
        "ar": "🌐 اختر اللغة"
    },
    "location_sim": {
        "en": "📍 Location Simulator",
        "ta": "📍 இருப்பிட சிமுலேட்டர்",
        "hi": "📍 स्थान सिम्युलेटर",
        "es": "📍 Simulador de Ubicación",
        "fr": "📍 Simulateur d'Emplacement",
        "te": "📍 స్థాన సిమ్యులేటర్",
        "kn": "📍 ಸ್ಥಳ ಸಿಮ್ಯುಲೇಟರ್",
        "de": "📍 Standort-Simulator",
        "ja": "📍 ロケーションシミュレーター",
        "zh": "📍 位置模拟器",
        "it": "📍 Simulatore di Posizione",
        "ru": "📍 Симулятор местоположения",
        "ar": "📍 محاكي الموقع"
    },
    "quick_loc": {
        "en": "Quick Test Locations:",
        "ta": "விரைவு சோதனை இடங்கள்:",
        "hi": "त्वरित परीक्षण स्थान:",
        "es": "Ubicaciones de Prueba Rápida:",
        "fr": "Emplacements de Test Rapide :",
        "te": "త్వరిత పరీక్ష స్థానాలు:",
        "kn": "ತ್ವರಿತ ಪರೀಕ್ಷಾ ಸ್ಥಳಗಳು:",
        "de": "Schnelltest-Standorte:",
        "ja": "クイックテストロケーション:",
        "zh": "快速测试地点：",
        "it": "Posizioni di Test Rapido:",
        "ru": "Быстрые тестовые локации:",
        "ar": "مواقع الاختبار السريع:"
    },
    "flood_zone_btn": {
        "en": "🔴 Inside Flood Zone",
        "ta": "🔴 வெள்ளப் பகுதிக்குள்",
        "hi": "🔴 बाढ़ क्षेत्र के भीतर",
        "es": "🔴 Dentro de Zona de Inundación",
        "fr": "🔴 Dans la Zone Inondée",
        "te": "🔴 వరద ప్రాంతం లోపల",
        "kn": "🔴 ಪ್ರವಾಹ ಪ್ರದೇಶದ ಒಳಗೆ",
        "de": "🔴 Im Überschwemmungsgebiet",
        "ja": "🔴 洪水地域内",
        "zh": "🔴 洪灾区内",
        "it": "🔴 All'interno della Zona alluvionata",
        "ru": "🔴 В зоне затопления",
        "ar": "🔴 داخل منطقة الفيضان"
    },
    "safe_loc_btn": {
        "en": "🟢 Safe Location",
        "ta": "🟢 பாதுகாப்பான இடம்",
        "hi": "🟢 सुरक्षित स्थान",
        "es": "🟢 Ubicación Segura",
        "fr": "🟢 Emplacement Sûr",
        "te": "🟢 సురక్షిత ప్రాంతం",
        "kn": "🟢 ಸುರಕ್ಷಿತ ಸ್ಥಳ",
        "de": "🟢 Sicherer Ort",
        "ja": "🟢 安全な場所",
        "zh": "🟢 安全地点",
        "it": "🟢 Posizione Sicura",
        "ru": "🟢 Безопасное место",
        "ar": "🟢 مكان آمن"
    },
    "cancel_sos": {
        "en": "🛑 CANCEL SOS",
        "ta": "🛑 SOS ஐ ரத்து செய்",
        "hi": "🛑 SOS रद्द करें",
        "es": "🛑 CANCELAR SOS",
        "fr": "🛑 ANNULER SOS",
        "te": "🛑 SOS రద్దు చేయండి",
        "kn": "🛑 SOS ರದ್ದುಗೊಳಿಸಿ",
        "de": "🛑 SOS ABBRECHEN",
        "ja": "🛑 SOSをキャンセル",
        "zh": "🛑 取消求救信号",
        "it": "🛑 ANNULLA SOS",
        "ru": "🛑 ОТМЕНИТЬ SOS",
        "ar": "🛑 إلغاء النداء العاجل"
    },
    "trigger_sos": {
        "en": "🚨 TRIGGER EMERGENCY SOS",
        "ta": "🚨 அவசர SOS ஐத் தூண்டவும்",
        "hi": "🚨 आपातकालीन SOS ट्रिगर करें",
        "es": "🚨 ACTIVAR SOS DE EMERGENCIA",
        "fr": "🚨 DÉCLENCHER SOS D'URGENCE",
        "te": "🚨 అత్యవసర SOSని ట్రిగర్ చేయండి",
        "kn": "🚨 ತುರ್ತು SOS ಅನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ",
        "de": "🚨 NOTFALL-SOS AUSLÖSEN",
        "ja": "🚨 緊急SOSを発信",
        "zh": "🚨 触发紧急求救",
        "it": "🚨 ATTIVA SOS DI EMERGENZA",
        "ru": "🚨 ВКЛЮЧИТЬ ЭКСТРЕННЫЙ SOS",
        "ar": "🚨 تفعيل طوارئ الاستغاثة"
    },
    "current_cond": {
        "en": "Current Condition",
        "ta": "தற்போதைய நிலை",
        "hi": "वर्तमान स्थिति",
        "es": "Condición Actual",
        "fr": "Condition Actuelle",
        "te": "ప్రస్తుత పరిస్థితి",
        "kn": "ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ",
        "de": "Aktuelle Bedingung",
        "ja": "現在の状態",
        "zh": "当前状况",
        "it": "Condizione Attuale",
        "ru": "Текущее состояние",
        "ar": "الحالة الحالية"
    },
    
   "temperature": {
        "en": "Temperature",
        "ta": "வெப்பநிலை",
        "hi": "तापमान",
        "es": "Temperatura",
        "fr": "Température",
        "te": "ఉష్ణోగ్రత",
        "kn": "ತಾಪಮಾನ",
        "de": "Temperatur",
        "ja": "気温",
        "zh": "温度",
        "it": "Temperatura",
        "ru": "Температура",
        "ar": "درجة الحرارة"
    },
    "wind_speed": {
        "en": "Wind Speed",
        "ta": "காற்றின் வேகம்",
        "hi": "हवा की गति",
        "es": "Velocidad del Viento",
        "fr": "Vitesse du Vent",
        "te": "గాలి వేగం",
        "kn": "ಗಾಳಿಯ ವೇಗ",
        "de": "Windgeschwindigkeiten",
        "ja": "風速",
        "zh": "风速",
        "it": "Velocità del Vento",
        "ru": "Скорость ветра",
        "ar": "سرعة الرياح"
    },
    "active_hazards": {
        "en": "Active Hazard Zones",
        "ta": "செயலில் உள்ள ஆபத்து மண்டலங்கள்",
        "hi": "सक्रिय खतरे के क्षेत्र",
        "es": "Zonas de Peligro Activas",
        "fr": "Zones de Danger Actives",
        "te": "సక్రియ ప్రమాద ప్రాంతాలు",
        "kn": "ಸಕ್ರಿಯ ಅಪಾಯ ವಲಯಗಳು",
        "de": "Aktive Gefahrenzonen",
        "ja": "アクティブな危険区域",
        "zh": "活动危险区",
        "it": "Zone di Pericolo Attive",
        "ru": "Активные опасные зоны",
        "ar": "مناطق الخطر النشطة"
    },
    "live_map_title": {
        "en": "🗺️ Live Hazard Map & Shelter Locations",
        "ta": "🗺️ நேரலை ஆபத்து வரைபடம் & தங்குமிடங்கள்",
        "hi": "🗺️ लाइव खतरा मानचित्र और आश्रय स्थल",
        "es": "🗺️ Mapa de Peligros y Refugios en Vivo",
        "fr": "🗺️ Carte des Dangers et Refuges en Direct",
        "te": "🗺️ లై లైవ్ హజార్డ్ మ్యాప్ & ఆశ్రయ స్థానాలు",
        "kn": "🗺️ ಲೈವ್ ಅಪಾಯ ನಕ್ಷೆ ಮತ್ತು ಆಶ್ರಯ ಸ್ಥಳಗಳು",
        "de": "🗺️ Live-Gefahrenkarte & Schutzräume",
        "ja": "🗺️ ライブハザードマップと避難所",
        "zh": "🗺️ 实时灾害地图与避难所位置",
        "it": "🗺️ Mappa dei Pericoli in Tempo Reale e Rifugi",
        "ru": "🗺️ Карта опасностей в реальном времени и убежища",
        "ar": "🗺️ خريطة المخاطر الحية ومواقع الملاجئ"
    },
    "nearest_havens": {
        "en": "🏥 Nearest Safe Havens",
        "ta": "🏥 அருகிலுள்ள பாதுகாப்பான அடைக்கலங்கள்",
        "hi": "🏥 निकटतम सुरक्षित आश्रय",
        "es": "🏥 Refugios Seguros Más Cercanos",
        "fr": "🏥 Refuges Sûrs les Plus Proches",
        "te": "🏥 సమీప సురక్షిత ఆశ్రయాలు",
        "kn": "🏥 ಹತ್ತಿರದ ಸುರಕ್ಷಿತ ಆಶ್ರಯಗಳು",
        "de": "🏥 Nächstgelegene sichere Zufluchtsorte",
        "ja": "🏥 最寄りの安全な避難所",
        "zh": "🏥 最近的安全避难所",
        "it": "🏥 Rifugi Sicuri più Vicini",
        "ru": "🏥 Ближайшие безопасные убежища",
        "ar": "🏥 أقرب الملاجئ الآمنة"
    },
    "active_warnings": {
        "en": "⚠️ Active Area Hazard Warnings",
        "ta": "⚠️ செயலில் உள்ள பகுதி ஆபத்து எச்சரிக்கைகள்",
        "hi": "⚠️ सक्रिय क्षेत्र खतरा चेतावनियाँ",
        "es": "⚠️ Advertencias de Peligro en Área Activa",
        "fr": "⚠️ Avertissements de Danger en Zone Active",
        "te": "⚠️ సక్రియ ప్రాంత ప్రమాద హెచ్చరికలు",
        "kn": "⚠️ ಸಕ್ರಿಯ ಪ್ರದೇಶದ ಅಪಾಯದ ಎಚ್ಚರಿಕೆಗಳು",
        "de": "⚠️ Aktive Gefahrenwarnungen für das Gebiet",
        "ja": "⚠️ 地域のアクティブな危険警告",
        "zh": "⚠️ 活动区域灾害警告",
        "it": "⚠️ Avvisi di Pericolo dell'Area Attiva",
        "ru": "⚠️ Активные предупреждения об опасности в районе",
        "ar": "⚠️ تحذيرات المخاطر النشطة في المنطقة"
    },
    "navigate_here": {
        "en": "🗺️ Navigate Here",
        "ta": "🗺️ இங்கு செல்லவும்",
        "hi": "🗺️ यहाँ नेविगेट करें",
        "es": "🗺️ Navegar Aquí",
        "fr": "🗺️ Naviguer Ici",
        "te": "🗺️ ఇక్కడకు నావిగేట్ చేయండి",
        "kn": "🗺️ ಇಲ್ಲಿಗೆ ನ್ಯಾವಿಗೇಟ್ ಮಾಡಿ",
        "de": "🗺️ Hierher navigieren",
        "ja": "🗺️ ここへ移動",
        "zh": "🗺️ 导航到此处",
        "it": "🗺️ Naviga Qui",
        "ru": "🗺️ Проложить маршрут сюда",
        "ar": "🗺️ التنقل إلى هنا"
    }
}
def get_ui_text(key: str, lang_name: str) -> str:
    """Retrieves localized UI text based on language name."""
    lang_code_map = {
        "English": "en",
        "Tamil": "ta",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "Telugu": "te",
        "Kannada": "kn",
        "German": "de",
        "Japanese": "ja",
        "Mandarin": "zh",
        "Italian": "it",
        "Russian": "ru",
        "Arabic": "ar"
    }
    code = lang_code_map.get(lang_name, "en")
    return UI_STRINGS.get(key, {}).get(code, UI_STRINGS.get(key, {}).get("en", ""))
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
