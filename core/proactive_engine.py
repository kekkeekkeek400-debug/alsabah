"""
Proactive Follow-up Engine ⏰
محرك المتابعة الاستباقية: يعمل في الخلفية 24/7.
يقوم بمراقبة العملاء الذين يسألون عن المنتجات ويختفون، ثم يراسلهم تلقائياً بعروض ترويجية لزيادة المبيعات!
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# قاعدة بيانات مؤقتة لتتبع العملاء المترددين
pending_carts = {}
scheduler = BackgroundScheduler()

def trigger_follow_up(user_id: str, product_intent: str):
    print(f"\n⏰ [Proactive Engine] تفعيل المتابعة للعميل: {user_id}")
    # في الإنتاج، هذه الدالة ستقوم بالاتصال بـ WhatsApp API وإرسال رسالة فعلية
    print(f"💬 [رسالة وتساب صامتة] إرسال: 'أهلاً بك مجدداً! لاحظت اهتمامك بـ ({product_intent})، ما رأيك بهذا الخصم الإضافي 10% (VIP10) لإتمام طلبك الآن؟'\n")

def schedule_proactive_followup(user_id: str, product_intent: str, delay_minutes: int = 120):
    """
    جدولة المتابعة الاستباقية للعميل.
    في الإنتاج نضعها بعد (ساعتين) مثلاً. قمنا بضبطها لتعمل كاختبار.
    """
    run_time = datetime.now() + timedelta(minutes=delay_minutes)
    
    # إلغاء أي رسالة متابعة قديمة لنفس العميل لكي لا نزعجه بكثرة الرسائل
    if user_id in pending_carts:
        scheduler.remove_job(pending_carts[user_id])
        
    job = scheduler.add_job(
        trigger_follow_up, 
        'date', 
        run_date=run_time, 
        args=[user_id, product_intent]
    )
    pending_carts[user_id] = job.id
    print(f"⏳ [Proactive Engine] تم رصد اهتمام العميل {user_id}. ستعمل المتابعة التلقائية في: {run_time.strftime('%H:%M:%S')}")

def start_proactive_scheduler():
    scheduler.start()
    print("🚀 [Proactive Engine] محرك المتابعة الاستباقية يعمل الآن في الخلفية لحصد المبيعات!")
