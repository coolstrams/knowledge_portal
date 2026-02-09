from langgraph.graph import StateGraph
from app.graph.state import RAGState
from app.graph.nodes.memory import load_memory_node
from app.graph.nodes.retrieve import retrieve_node
from app.graph.nodes.prompt import prompt_node

graph = StateGraph(RAGState)

graph.add_node("memory", load_memory_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("prompt", prompt_node)

graph.set_entry_point("memory")
graph.add_edge("memory", "retrieve")
graph.add_edge("retrieve", "prompt")

rag_app = graph.compile()


async def run_rag_graph(session_id: str, query: str):
    return await rag_app.ainvoke({
        "session_id": session_id,
        "query": query
    })
