import json
from app.core.redis import redis_client
from app.graph.state import RAGState


def load_memory_node(state: RAGState):
    key = f"rag:chat:{state['session_id']}"
    history = redis_client.lrange(key, 0, -1)
    state["history"] = [json.loads(x) for x in history]
    return state
