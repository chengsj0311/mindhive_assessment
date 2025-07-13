from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agents.planner import chat_app 

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    messages = [HumanMessage(req.message)]
    config = {"configurable": {"thread_id": req.session_id}}
    try:
        out = chat_app.invoke({"messages": messages}, config)
        ai_msgs = out.get("messages", [])
        if not ai_msgs:
            raise HTTPException(500, "AI returned no message")
        ai_msg = ai_msgs[-1]
        return ChatResponse(response=ai_msg.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in /chat: {e}")
