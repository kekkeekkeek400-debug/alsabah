"""
The Python Deep Brain Server 🧠🐍 (Omniscient V5)
خادم بايثون العبقري الذي يستقبل الرسائل، يتصفح الإنترنت الحي، ويبادر بمراسلة العملاء!
"""

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from core.langchain_engine import process_with_agents
from core.vision_engine import analyze_product_image
from core.critic_agent import self_correct_response
from tools.voice_generator import generate_voice_note
from core.proactive_engine import start_proactive_scheduler
# pyrefly: ignore [missing-import]
import uvicorn

app = FastAPI(title="Quantum Omniscient Brain V5", description="God-Mode Multimodal AI Engine with Live Web")

# إقلاع محركات الخلفية عند تشغيل السيرفر
@app.on_event("startup")
def startup_event():
    start_proactive_scheduler()

class MessagePayload(BaseModel):
    user_id: str
    message: str
    chat_history: list = []
    need_voice: bool = False
    system_prompt: str = "أنت مساعد ذكي."

class VisionPayload(BaseModel):
    user_id: str
    image_base64: str
    prompt: str = "تعرف على هذا المنتج واذكر تفاصيله:"

@app.get("/")
def health_check():
    return {"status": "Titan Omniscient Python Brain V5 is Online", "capabilities": ["Text", "Vision", "Voice", "WebSurfer", "Proactive"]}

@app.post("/think")
async def deep_think(payload: MessagePayload):
    try:
        print(f"\n🧠 [Omniscient Brain] استلام طلب من العميل {payload.user_id}...")
        
        # 1. التفكير المتعدد (بما في ذلك التصفح الحي إن احتاجه)
        raw_response = await process_with_agents(
            message=payload.message, 
            history=payload.chat_history,
            user_id=payload.user_id,
            system_prompt=payload.system_prompt
        )
        
        # 2. النقد الذاتي (Self-Healing Critic)
        final_text = await self_correct_response(payload.message, raw_response)
        
        # 3. محرك الصوت البشري
        voice_base64 = None
        if payload.need_voice:
            voice_base64 = generate_voice_note(final_text)
            
        print("✅ [Omniscient Brain] اكتملت الدورة الفائقة بنجاح!")
        return {
            "response": final_text,
            "voice_data": voice_base64,
            "verified_by_critic": True
        }
        
    except Exception as e:
        print(f"❌ Error in Deep Brain V5: {e}")
        raise HTTPException(status_code=500, detail="فشل في المعالجة الفائقة")

@app.post("/vision")
async def analyze_vision(payload: VisionPayload):
    try:
        description = analyze_product_image(payload.image_base64, payload.prompt)
        return {"description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 جاري إقلاع محرك Omniscient V5...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
