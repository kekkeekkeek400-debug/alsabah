"""
Multimodal Vision Engine 👁️
يقوم بتحليل أي صورة مرسلة من العميل على الواتساب للتعرف على المنتجات بصرياً.
"""

# pyrefly: ignore [missing-import]
from google.generativeai import GenerativeModel
# pyrefly: ignore [missing-import]
import google.generativeai as genai
# pyrefly: ignore [missing-import]
from PIL import Image
import io
import base64
import os

def analyze_product_image(image_base64: str, prompt: str = "تعرف على هذا المنتج واذكر أسبابه ومواصفاته بالتفصيل:") -> str:
    """
    سحب الصورة وتحليلها من خلال نموذج Gemini Vision الخارق
    """
    try:
        print("👁️ [Vision Engine] جاري الفحص البصري للصورة المرسلة من العميل...")
        
        # فك تشفير الصورة من base64
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))

        # تشغيل نموذج Gemini Flash/Pro Vision
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "تعذر تحليل الصورة: مفتاح API غير معرف."
            
        genai.configure(api_key=api_key)
        model = GenerativeModel('gemini-flash-latest')
        
        response = model.generate_content([prompt, image])
        print("✅ [Vision Engine] تم استخراج المعالم البصرية بنجاح!")
        return response.text

    except Exception as e:
        print(f"❌ Error analyzing vision: {e}")
        return "حدث خطأ أثناء قراءة معالم الصورة بكتالوج المنتجات."
