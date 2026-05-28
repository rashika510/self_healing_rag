from typing import List, Dict


class PineconeRetriever:
    def retrieve(self, query: str) -> List[Dict]:
        return [
            {"text": f"Relevant context for: {query}", "score": 0.82},
            {"text": f"Supporting detail for: {query}", "score": 0.77},
        ]