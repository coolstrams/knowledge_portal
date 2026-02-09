from app.graph.state import RAGState


def prompt_node(state: RAGState):
    messages = []

    for h in state.get("history", []):
        messages.append((h["role"], h["content"]))

    messages.append((
        "system",
        f"请基于以下知识回答用户问题：\n{state.get('context', '')}"
    ))
    messages.append(("user", state["query"]))

    state["messages"] = messages
    return state
