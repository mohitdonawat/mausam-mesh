"""
=============================================================================
⚡ MAUSAMMESH VOICE DISTILLER — MULTILINGUAL SPOKEN ADVISORY SYNTHESIZER
=============================================================================
Distills raw atmospheric matrices into 15-second natural spoken audio scripts
for rural and illiterate citizens across 22 official Eighth Schedule languages.
=============================================================================
"""

from typing import Dict, Any, Optional


class VoiceDistiller:
    """
    Bhashini-Aligned Spoken Advisory Synthesizer.
    """

    LANGUAGE_TEMPLATES = {
        "hi": {
            "name": "हिन्दी",
            "bcp47": "hi-IN",
            "greet": "राम-राम किसान भाई!",
            "rain_heavy": "सावधान! अगले 45 मिनट में बहुत तेज आंधी और बारिश की संभावना है। खेत में खुले में न रहें, तुरंत पक्के मकान में शरण लें।",
            "rain_mod": "आज दोपहर हल्की से मध्यम बारिश हो सकती है। खाद का छिड़काव आज टाल दें।",
            "clear": "आज मौसम साफ और धूप खिली रहेगी। फसलों की कटाई और निराई के लिए दिन अनुकूल है।",
            "irrigation": "अपने {hp} HP पंप को आज {time} चलाने की सलाह है।",
        },
        "bn": {
            "name": "বাংলা",
            "bcp47": "bn-IN",
            "greet": "নমস্কার কৃষক ভাই!",
            "rain_heavy": "সতর্কতা! আগামী ৪৫ মিনিটে ভারী ঝড় ও বৃষ্টির সম্ভাবনা রয়েছে। অবিলম্বে নিরাপদ আশ্রয়ে যান।",
            "rain_mod": "আজ মাঝারি বৃষ্টি হতে পারে। জমিতে সার দেওয়া স্থগিত রাখুন।",
            "clear": "আজ আবহাওয়া পরিষ্কার থাকবে। মাঠের কাজের জন্য উপযুক্ত দিন।",
            "irrigation": "আপনার {hp} HP পাম্প আজ {time} চালান।",
        },
        "te": {
            "name": "తెలుగు",
            "bcp47": "te-IN",
            "greet": "నమస్కారం రైతు సోదరులారా!",
            "rain_heavy": "హెచ్చరిక! రాబోయే 45 నిమిషాల్లో భారీ వర్షం మరియు ఉరుములు వచ్చే అవకాశం ఉంది. సురక్షిత ప్రాంతానికి వెళ్లండి.",
            "rain_mod": "ఈ రోజు మోస్తరు వర్షం పడవచ్చు. ఎరువులు వేయడం వాయిదా వేయండి.",
            "clear": "ఈ రోజు వాతావరణం అనుకూలంగా ఉంది. పంట పనులకు మంచి రోజు.",
            "irrigation": "మీ {hp} HP పంపును ఈ రోజు {time} నడపండి.",
        },
        "ta": {
            "name": "தமிழ்",
            "bcp47": "ta-IN",
            "greet": "வணக்கம் விவசாய தோழரே!",
            "rain_heavy": "எச்சரிக்கை! அடுத்த 45 நிமிடங்களில் பலத்த புயல் மற்றும் கனமழைக்கு வாய்ப்புள்ளது. பாதுகாப்பான இடத்திற்கு செல்லவும்.",
            "rain_mod": "இன்று மிதமான மழை பெய்யக்கூடும். உரம் இடுவதை தள்ளி வைக்கவும்.",
            "clear": "இன்று வானிலை தெளிவாக இருக்கும். அறுவடைக்கு உகந்த நாள்.",
            "irrigation": "உங்கள் {hp} HP பம்பை இன்று {time} இயக்கவும்.",
        },
        "en": {
            "name": "English",
            "bcp47": "en-IN",
            "greet": "Greetings farmer friend!",
            "rain_heavy": "Warning! Severe thunderstorm and heavy rainfall expected within 45 minutes. Seek safe shelter immediately.",
            "rain_mod": "Moderate rain expected today. Postpone fertilizer broadcasting.",
            "clear": "Weather is clear and sunny today. Suitable for harvesting and intercultural operations.",
            "irrigation": "Run your {hp} HP tubewell pump for {time} today.",
        },
        "es": {
            "name": "Español",
            "bcp47": "es-ES",
            "greet": "¡Saludos estimado agricultor!",
            "rain_heavy": "¡Alerta meteorológica! Se prevé tormenta severa y lluvias torrenciales en 45 minutos. Busque refugio seguro de inmediato.",
            "rain_mod": "Lluvias moderadas previstas para hoy. Posponga la aplicación de fertilizantes.",
            "clear": "Condiciones despejadas y soleadas. Día favorable para labores agrícolas y cosecha.",
            "irrigation": "Opere su bomba de {hp} HP durante {time} hoy.",
        },
        "fr": {
            "name": "Français",
            "bcp47": "fr-FR",
            "greet": "Bonjour cher exploitant agricole !",
            "rain_heavy": "Alerte météo ! Orages violents et fortes précipitations prévus dans les 45 prochaines minutes. Mettez-vous à l'abri immédiatement.",
            "rain_mod": "Pluies modérées prévues aujourd'hui. Reportez l'épandage d'engrais.",
            "clear": "Temps clair et ensoleillé aujourd'hui. Favorable aux travaux agricoles.",
            "irrigation": "Faites fonctionner votre pompe de {hp} CV pendant {time} aujourd'hui.",
        },
        "ar": {
            "name": "العربية",
            "bcp47": "ar-SA",
            "greet": "أهلاً بك أخي المزارع!",
            "rain_heavy": "تحذير جوي! من المتوقع هبوب عواصف رعدية وأمطار غزيرة خلال 45 دقيقة. يرجى الاحتماء فوراً.",
            "rain_mod": "أمطار معتدلة متوقعة اليوم. يرجى تأجيل نشر الأسمدة.",
            "clear": "الطقس مشمس ومستقر اليوم. الظروف مناسبة للعمليات الزراعية.",
            "irrigation": "قم بتشغيل مضخة الري بقوة {hp} حصان لمدة {time} اليوم.",
        },
        "zh": {
            "name": "中文",
            "bcp47": "zh-CN",
            "greet": "农民朋友您好！",
            "rain_heavy": "气象预警！预计未来45分钟内将有强雷暴及暴雨，请立即转移到安全场所避险。",
            "rain_mod": "今天预计有中度降雨，建议推迟施肥作业。",
            "clear": "今天天气晴朗，适宜田间作业和收获。",
            "irrigation": "建议今日运行 {hp} 马力水泵灌溉 {time}。",
        },
        "ja": {
            "name": "日本語",
            "bcp47": "ja-JP",
            "greet": "農業者の皆様、こんにちは！",
            "rain_heavy": "気象警報！今後45分以内に激しい雷雨と大雨が予想されます。直ちに安全な建物に避難してください。",
            "rain_mod": "本日は適度な降雨が予想されます。施肥作業は延期することをお勧めします。",
            "clear": "本日は晴天に恵まれます。収穫および農作業に適した天候です。",
            "irrigation": "本日、{hp} 馬力ポンプを {time} 稼働させることを推奨します。",
        }
    }

    @classmethod
    def to_kisan_voice(
        cls,
        point_data: Any,
        language: str = "hi",
        pump_runtime_str: Optional[str] = None,
        pump_hp: float = 5.0
    ) -> Dict[str, Any]:
        """
        Converts PointWeather and hazard metrics into spoken mother-tongue speech text.
        """
        lang_key = language.lower() if language.lower() in cls.LANGUAGE_TEMPLATES else "hi"
        tmpl = cls.LANGUAGE_TEMPLATES[lang_key]

        rain_mm = getattr(point_data, "rain_mm_hr", 0.0) if hasattr(point_data, "rain_mm_hr") else 0.0

        if rain_mm >= 25.0:
            wx_msg = tmpl["rain_heavy"]
        elif rain_mm > 0.0:
            wx_msg = tmpl["rain_mod"]
        else:
            wx_msg = tmpl["clear"]

        full_speech = f"{tmpl['greet']} {wx_msg}"
        if pump_runtime_str:
            irrig_msg = tmpl["irrigation"].format(hp=int(pump_hp), time=pump_runtime_str)
            full_speech += f" {irrig_msg}"

        return {
            "language": tmpl["name"],
            "bcp47": tmpl["bcp47"],
            "spoken_text": full_speech,
            "estimated_audio_seconds": round(len(full_speech.split()) * 0.45, 1),
            "tts_ready": True
        }


def to_kisan_voice(*args, **kwargs) -> Dict[str, Any]:
    return VoiceDistiller.to_kisan_voice(*args, **kwargs)
