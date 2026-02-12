from langgraph.graph import StateGraph
from app.graph.state import RAGState
from app.graph.nodes.memory import load_memory_node
from app.graph.nodes.retrieve import retrieve_node
from app.graph.nodes.prompt import prompt_node
from app.schemas.chat import ChatMessageItem

graph = StateGraph(RAGState)

graph.add_node("memory", load_memory_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("prompt", prompt_node)

graph.set_entry_point("memory")
graph.add_edge("memory", "retrieve")
graph.add_edge("retrieve", "prompt")

rag_app = graph.compile()


async def run_rag_graph_old(session_id: str, query: str):
    return await rag_app.ainvoke(
        {"session_id": session_id, "query": query}
    )


async def run_rag_graph_old2(messages: list[ChatMessageItem], session_id: str):
    return await rag_app.ainvoke(
        {"messages": messages, "session_id": session_id}
    )


async def run_rag_graph(messages: list[ChatMessageItem], session_id: str, query: str):
    prompt_tokens = 0
    completion_tokens = 0
    # query = next(
    #     m.content for m in reversed(messages) if m.role == "user"
    # )
    async for chunk in rag_app.astream(
        {"messages": messages, "session_id": session_id, "query": query},
        stream_mode="messages"
    ):
        # for msg in chunk.get("messages", []):
        #     if msg.content:
        #         completion_tokens += 1
        #         yield msg.content
        if chunk.content:
            completion_tokens += 1
            yield chunk.content

        # if event["event"] == "on_chain_start":
        #     prompt_tokens = event["data"]["prompt_tokens"]
        #
        # if event["event"] == "on_chain_stream":
        #     completion_tokens += 1
        #     yield event["data"]["token"]

    yield {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }
