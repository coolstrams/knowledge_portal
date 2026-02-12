import json
from app.core.redis import redis_client
from app.graph.state import RAGState


def load_memory_node(state: RAGState):
    session_id = state.get("session_id")
    if not session_id:
        raise ValueError("RAGState must contain 'session_id'")
    key = f"rag:chat:{session_id}"

    history = redis_client.lrange(key, 0, -1)
    # Redis 返回 bytes，需要 decode
    if not history:
        state["history"] = [json.loads(x.decode("utf-8")) for x in history]

    return state
