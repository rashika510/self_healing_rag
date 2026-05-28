from fastapi import FastAPI, HTTPException
from app.schemas.models import ChatRequest, ChatResponse, FeedbackRequest
from app.rag.orchestrator import SelfHealingRAG

app = FastAPI(title="Self-Healing RAG Pipeline", version="1.0.0")
rag = SelfHealingRAG()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        return rag.answer(req.query, req.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    return {"received": True, "query_id": req.query_id, "label": req.label}