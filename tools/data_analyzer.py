"""
Dynamic Data Analyzer Tool
يقوم بتحليل وقراءة أي بيانات أو كتالوجات منتجات مرفوعة ديناميكياً من التاجر بدون أي بيانات وهمية مسبقة.
"""

import pandas as pd
import json
import os

def analyze_company_data(query: str, data_source_path: str = None) -> str:
    """
    تقوم هذه الدالة بقراءة ملف البيانات المرفوع من قبل العميل/التاجر (CSV أو Excel أو JSON) وتصفيتها ديناميكياً.
    """
    print(f"📊 [Data Analyzer] جاري البحث في كتالوج التاجر عن: {query}")
    
    # إذا لم يقم التاجر برفع ملف منتجات خاص به بعد
    if not data_source_path or not os.path.exists(data_source_path):
        return "ملاحظة: التاجر لم يقم برفع جدول منتجات خاص به حتى الآن. يمكنك الرد بالمعلومات العامة أو طلب انتظار الموظف."
        
    try:
        # قراءة ملف التاجر تلقائياً وبشكل ديناميكي حسب صيغته
        if data_source_path.endswith('.csv'):
            df = pd.read_csv(data_source_path)
        elif data_source_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(data_source_path)
        elif data_source_path.endswith('.json'):
            df = pd.read_json(data_source_path)
        else:
            return "صيغة ملف كتالوج التاجر غير مدعومة."

        # تصفية الجدول ديناميكياً بناءً على كلمات العميل
        query_words = query.lower().split()
        matched_rows = df[df.apply(lambda row: any(word in str(row.values).lower() for word in query_words), axis=1)]

        if matched_rows.empty:
            return "لم نجد هذا المنتج في كتالوج التاجر الحقيقي."

        # استخراج أول 3 نتائج مطابقة وتحويلها لـ JSON
        results = matched_rows.head(3).to_dict(orient='records')
        return f"بيانات المنتجات من كتالوج التاجر الحقيقي: {json.dumps(results, ensure_ascii=False)}"

    except Exception as e:
        print(f"❌ خطأ أثناء قراءة كتالوج التاجر: {e}")
        return "حدث خطأ أثناء قراءة ملف المنتجات الخاص بالتاجر."
