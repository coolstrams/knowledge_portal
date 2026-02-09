from typing import TypedDict, List, Any


class RAGState(TypedDict, total=False):
    session_id: str
    query: str
    history: List[dict]
    context: str
    messages: list
    answer: Any
