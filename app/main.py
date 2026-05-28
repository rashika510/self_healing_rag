from fastapi import FastAPI
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.feedback import router as feedback_router

app = FastAPI(title="Self-Healing RAG Pipeline", version="1.0.0")

@app.get("/", tags=["root"])
def read_root():
	return {"message": "Self-Healing RAG API. Visit /docs for API docs."}

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(feedback_router)