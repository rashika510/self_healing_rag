from fastapi import APIRouter, HTTPException
from app.schemas.models import ChatRequest, ChatResponse
from app.rag.orchestrator import SelfHealingRAG

router = APIRouter(tags=["chat"])
rag = SelfHealingRAG()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        return rag.answer(req.query, req.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))