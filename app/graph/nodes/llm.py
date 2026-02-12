import os
from langchain_openai import ChatOpenAI
from app.graph.state import RAGState

llm = ChatOpenAI(
    # model="gpt-4o-mini",
    model="qwen-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
    stream_usage=True
)


async def llm_stream(state: RAGState):
    full_message = None
    async for chunk in llm.astream(state["messages"], stream_usage=True):
        if full_message is None:
            full_message = chunk
        else:
            full_message += chunk
        if chunk.content:
            yield chunk.content

    print(full_message.usage_metadata)

    input_tokens = full_message.usage_metadata["input_tokens"]
    output_tokens = full_message.usage_metadata["output_tokens"]
    total_tokens = full_message.usage_metadata["total_tokens"]

    yield {
        "prompt_tokens": input_tokens,
        "completion_tokens": output_tokens,
        "total_tokens": total_tokens,
    }
