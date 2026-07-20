"""
Voice Synthesis Engine 🎙️🔊
تحويل النصوص إلى مقاطع صوتية (Voice Notes) طبيعية بشرية للرد على العميل صوتاً.
"""

# pyrefly: ignore [missing-import]
from gtts import gTTS
import base64
import io

def generate_voice_note(text_content: str, lang: str = 'ar') -> str:
    """
    يحول النص إلى مقطع صوتي بصيغة Base64 ليتم إرساله عبر الواتساب.
    """
    try:
        print(f"🎙️ [Voice Generator] جاري توليد مقطع صوتي للنص: {text_content[:30]}...")
        
        # استخدام gTTS لتوليد الصوت
        tts = gTTS(text=text_content, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # تحويل الصوت لـ Base64
        audio_base64 = base64.b64encode(fp.read()).decode('utf-8')
        print("✅ [Voice Generator] تم إعداد الملف الصوتي البشري بنجاح!")
        return audio_base64
        
    except Exception as e:
        print(f"❌ Error generating voice: {e}")
        return None
