import httpx
from app.graph.state import RAGState
from app.core.config import KB_SEARCH_URL


async def retrieve_node(state: RAGState):
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            KB_SEARCH_URL,
            json={
                # "query": state["query"],
                "query": "什么是 LangChain",
                "top_k": 3
            }
        )
        resp.raise_for_status()
        data = resp.json()

    state["context"] = "\n".join(
        item["content"] for item in data
    )
    return state
