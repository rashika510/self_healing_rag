import os
from dataclasses import dataclass

@dataclass
class Settings:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "rag-index")
    pinecone_namespace: str = os.getenv("PINECONE_NAMESPACE", "default")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.75"))

settings = Settings()