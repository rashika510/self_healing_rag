from typing import List


class ClaudeService:
    def expand_query(self, query: str) -> List[str]:
        return [query, f"{query} in detail", f"best answer for {query}"]

    def generate_answer(self, query: str, context: str) -> str:
        return f"Answer based on retrieved context for: {query}\n\n{context}"