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
    async for chunk in llm.astream(state["messages"]):
        if chunk.content:
            yield chunk.content
