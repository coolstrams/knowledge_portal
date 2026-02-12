from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.graph.rag_graph import run_rag_graph_old
from app.graph.nodes.llm import llm_stream
from app.utils.sse import sse_json_event
from app.utils.id import gen_datetime_uuid16

router = APIRouter(tags=["chat"])


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):

    async def generator():
        # ✅ 按 yyyymmdd + uuid 生成
        conversation_id = gen_datetime_uuid16()
        message_id = gen_datetime_uuid16()

        try:
            state = await run_rag_graph_old(
                query=req.query,
                session_id=req.session_id,
            )

            async for token in llm_stream(state):
                yield sse_json_event(
                    token=token,
                    conversation_id=conversation_id,
                    session_id=req.session_id,
                    message_id=message_id,
                    parent_message_id=""
                )

            # 🔚 流结束标识（推荐）
            yield f'data: {{"type":"done","conversationID":"{conversation_id}","messageID":"{message_id}"}}\n\n'

        except Exception as e:
            yield sse_json_event(
                token=f"[ERROR] {str(e)}",
                conversation_id=conversation_id,
                session_id=req.session_id,
                message_id=message_id,
                parent_message_id=""
            )

    return StreamingResponse(
        generator(),
        media_type="text/event-stream"
    )
