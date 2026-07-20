"""
Self-Healing Critic Agent 🔄 (Powered by Groq ⚡)
وكيل النقد الذاتي سريع جداً يعمل على نموذج Llama-3 للتدقيق اللحظي قبل إرسال الرسالة للعميل.
"""

# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
import os

# استخدام نموذج Groq السريع والمجاني للتدقيق اللغوي والمعلوماتي
critic_llm = ChatGroq(model="llama3-8b-8192", temperature=0.0)

async def self_correct_response(original_query: str, generated_response: str) -> str:
    """
    تقوم هذه الدالة بنقد وتدقيق الإجابة وإصلاح أي خطأ صياغي أو معلوماتي آلياً.
    """
    print("🕵️ [Critic Agent] جاري المراجعة والتدقيق الذاتي للرد (via Groq)...")
    
    prompt = f"""أنت محرر ودقيق لغوي ومهني لبوتات المبيعات.
سؤال العميل: "{original_query}"
الرد المقترح من البوت: "{generated_response}"

مهمتك:
1. تأكد أن الرد خالي من التناقض أو الأخطاء.
2. إذا كان الرد ممتازاً ومؤدباً، أعد إرساله كما هو.
3. إذا كان يحتاج تحسيناً أو اختصاراً، أعد صياغته ليكون بأعلى جودة ممكنة.

أعد الرد النهائي فقط بدون مقدمات:"""

    try:
        corrected = await critic_llm.ainvoke(prompt)
        print("✅ [Critic Agent] تمت المراجعة والاعتماد.")
        return corrected.content
    except Exception as e:
        print(f"⚠️ Critic Engine fallback: {e}")
        return generated_response
