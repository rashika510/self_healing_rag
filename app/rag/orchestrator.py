from app.core.config import settings
from app.services.claude import ClaudeService
from app.retrievers.pincone_retriever import PineconeRetriever
from app.schemas.models import ChatResponse
from typing import Optional

class SelfHealingRAG:
    def __init__(self):
        self.claude = ClaudeService()
        self.retriever = PineconeRetriever()

    def answer(self, query: str, session_id: Optional[str] = None) -> ChatResponse:
        retrieval_path = ["primary"]
        docs = self.retriever.retrieve(query)
        confidence = max((d["score"] for d in docs), default=0.0)

        if confidence < settings.confidence_threshold:
            retrieval_path.append("expanded")
            expanded_queries = self.claude.expand_query(query)
            for q in expanded_queries[1:]:
                docs = self.retriever.retrieve(q)
                confidence = max(confidence, max((d["score"] for d in docs), default=0.0))
                if confidence >= settings.confidence_threshold:
                    break

        escalated = confidence < settings.confidence_threshold
        if escalated:
            return ChatResponse(
                answer="I’m not confident enough to answer. This case has been escalated for review.",
                confidence=confidence,
                retrieval_path=retrieval_path + ["escalated"],
                escalated=True,
            )

        context = "\n".join(d["text"] for d in docs)
        answer = self.claude.generate_answer(query, context)
        return ChatResponse(answer=answer, confidence=confidence, retrieval_path=retrieval_path, escalated=False)