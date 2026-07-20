"""
LangChain Orchestrator V5 (Powered by Groq LPU ⚡)
يدعم التصفح الحي، وتحليل العاطفة، والمتابعة الاستباقية بسرعة الضوء وبدون تكلفة!
"""

# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain.agents import AgentExecutor, create_structured_chat_agent
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.data_analyzer import analyze_company_data
from tools.web_search import search_live_internet
from core.proactive_engine import schedule_proactive_followup
# pyrefly: ignore [missing-import]
from langchain.tools import Tool
import os

groq_key = os.environ.get("GROQ_API_KEY", "dummy_key_to_prevent_crash")
llm = ChatGroq(model_name="llama3-70b-8192", temperature=0.2, groq_api_key=groq_key)

data_tool = Tool(
    name="DataAnalyzer",
    func=analyze_company_data,
    description="استخدم هذه الأداة للبحث في كتالوج التاجر عن أسعار ومواصفات المنتجات."
)

web_tool = Tool(
    name="WebSurfer",
    func=search_live_internet,
    description="استخدم هذه الأداة حصرياً للبحث عن الأخبار العاجلة، والأحداث الحية، وأسعار العملات اليومية من الإنترنت."
)

tools = [data_tool, web_tool]

system_msg = """{system_prompt}
تعليماتك الصارمة:
1. استخدم 'WebSurfer' دائماً لأي سؤال عن أسعار صرف الدولار، أو أخبار اليوم. لا تقم بالرد من ذاكرتك القديمة في هذه الأمور أبداً.
2. استخدم 'DataAnalyzer' إذا سأل العميل عن توفر بضاعة في متجرنا.
3. كن ودوداً جداً وقدم حلولاً ذكية تليق بمبيعات احترافية.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_msg),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 🧠 مسجل العاطفة (Sentiment Logger)
def log_sentiment(user_id: str, message: str, ai_response: str):
    sentiment = "محايد"
    if any(word in message for word in ["شكرا", "ممتاز", "رائع", "يعطيك العافية"]):
        sentiment = "إيجابي"
    elif any(word in message for word in ["سيء", "تاخير", "مشكلة", "غاضب"]):
        sentiment = "سلبي"
        
    log_entry = f"User: {user_id} | Emotion: {sentiment} | Length: {len(message)}\n"
    with open("sentiment_analytics.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

async def process_with_agents(message: str, history: list, user_id: str, system_prompt: str = "أنت مساعد ذكي.") -> str:
    if groq_key == "dummy_key_to_prevent_crash":
        return "⚠️ عذراً، لم تقم بوضع مفتاح GROQ_API_KEY في إعدادات Render بشكل صحيح، أو أنك نسيت حفظ التغييرات. يرجى العودة لموقع Render وإضافته."

    response = await agent_executor.ainvoke({
        "system_prompt": system_prompt,
        "input": message,
        "chat_history": history
    })
    
    final_output = response["output"]
    
    log_sentiment(user_id, message, final_output)
    
    if any(word in message for word in ["سعر", "بكم", "تفاصيل", "اريد", "شراء"]):
        schedule_proactive_followup(user_id, "منتج مجهول", delay_minutes=1)
        
    return final_output
