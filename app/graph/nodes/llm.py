import os
from langchain_openai import ChatOpenAI
from app.graph.state import RAGState

llm = ChatOpenAI(
    # model="gpt-4o-mini",
    model="qwen-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True
)


async def llm_stream(state: RAGState):
    config = {
        "stream_options": {"include_usage": True}
    }
    usage = None
    async for chunk in llm.astream(state["messages"], config=config):
        if chunk.content:
            yield chunk.content
        if chunk.response_metadata and "usage" in chunk.response_metadata:
            usage = chunk.response_metadata["usage"]

    prompt_token = usage["prompt_tokens"] if usage else None
    completion_token = usage["completion_tokens"] if usage else None
    total_token = usage["total_tokens"] if usage else None
