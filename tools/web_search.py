"""
Live Web Search Tool 🌍
أداة التصفح الحي: تمنح الذكاء الاصطناعي القدرة على الاتصال بالإنترنت والبحث في محرك (DuckDuckGo)
لجلب أحدث المعلومات اللحظية (أسعار عملات، أخبار عاجلة) ومنع الهلوسة بمعلومات قديمة.
"""

from langchain_community.tools import DuckDuckGoSearchRun

# إعداد متصفح الإنترنت السريع
search_tool = DuckDuckGoSearchRun()

def search_live_internet(query: str) -> str:
    """
    تقوم هذه الدالة بإجراء بحث حي في الإنترنت.
    """
    print(f"🌍 [Web Surfer] جاري تصفح الإنترنت الحي للبحث عن: {query}")
    try:
        # تشغيل المتصفح وسحب النتائج
        results = search_tool.invoke(query)
        print("✅ [Web Surfer] تم جلب أحدث المعلومات من الإنترنت بنجاح!")
        return f"نتائج البحث الحي من الإنترنت: {results}"
    except Exception as e:
        print(f"❌ خطأ أثناء الاتصال بالإنترنت: {e}")
        return "حدث خطأ أثناء محاولة الاتصال بالإنترنت الحي، لا يمكنني تأكيد الأخبار اللحظية الآن."
