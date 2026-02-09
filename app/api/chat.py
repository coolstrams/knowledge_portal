from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest
from app.graph.rag_graph import rag_app
from app.graph.nodes.llm import llm_stream
from app.core.redis import redis_client
import json

router = APIRouter()


@router.post("/stream")
async def chat_stream(req: ChatRequest):

    async def event_generator():
        state = {
            "session_id": req.session_id,
            "query": req.query
        }

        state = await rag_app.ainvoke(state)

        answer_chunks = []

        async for token in llm_stream(state):
            answer_chunks.append(token)
            yield f"data: {token}\n\n"

        # 保存历史
        key = f"rag:chat:{req.session_id}"
        redis_client.rpush(
            key,
            json.dumps({"role": "user", "content": req.query}),
            json.dumps({"role": "assistant", "content": "".join(answer_chunks)})
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
