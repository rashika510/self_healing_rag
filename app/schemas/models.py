from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    retrieval_path: List[str]
    escalated: bool


class FeedbackRequest(BaseModel):
    query_id: str
    label: str
    notes: Optional[str] = None
