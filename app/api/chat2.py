# app/api/chat.py
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app.core.database import get_db
from app.models.chat_conversation import ChatConversation, ChatConversationDao
from app.models.chat_message import ChatMessage, ChatMessageDao
from app.utils.id import gen_datetime_uuid16
from app.graph.rag_graph import run_rag_graph, run_rag_graph_old2
from app.schemas.chat import ChatRequest

router = APIRouter()


@router.post("/stream")
async def chat_stream(req: ChatRequest, db: Session = Depends(get_db)):
    user_id = req.session_id

    conversation_id = req.conversationID
    parent_message_id = req.parentMessageID
    messages = req.messages

    user_content = next(
        m.content for m in reversed(messages) if m.role == "user"
    )

    is_new_conversation = not conversation_id

    if is_new_conversation:
        conversation_id = gen_datetime_uuid16()
        ChatConversationDao.create_conversation(ChatConversation(
            user_id=user_id,
            conversation_id=conversation_id,
            type="rag",
            category="knowledge",
            title=user_content[:50],
        ))

        # 写入用户消息
        user_msg_id = gen_datetime_uuid16()

        db.add(ChatMessage(
            user_id=user_id,
            conversation_id=conversation_id,
            message_id=user_msg_id,
            is_bot=False,
            type="question",
            category="knowledge",
            content=user_content,
        ))
        db.commit()

        # 创建 assistant 消息
        assistant_msg_id = gen_datetime_uuid16()

        assistant_msg = ChatMessage(
            user_id=user_id,
            conversation_id=conversation_id,
            message_id=assistant_msg_id,
            is_bot=True,
            type="answer",
            category="knowledge",
            content="",
        )
        db.add(assistant_msg)
        db.commit()

    async def event_generator():
        full_answer = ""

        async for token in run_rag_graph(messages=messages, session_id=user_id, query=user_content):
            if isinstance(token, str):
                full_answer += token

                data = {
                    'data': {'content': token},
                    'meta': {
                        'conversationID': conversation_id,
                        'parentMessageID': parent_message_id or '',
                        'messageID': assistant_msg_id,
                        'sessionID': user_id
                    },
                    'type': 'answer'
                }

                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                # 更新 assistant 消息
                assistant_msg.content = full_answer
                db.add(assistant_msg)
                db.commit()

            elif isinstance(token,  dict):
                prompt_tokens = token["prompt_tokens"]
                completion_tokens = token["completion_tokens"]
                total_tokens = token["total_tokens"]

                bot_data = {
                    'meta': {
                        'conversationID': conversation_id,
                        'parentMessageID': parent_message_id or user_msg_id,
                        'messageID': assistant_msg_id,
                        'promptTokens': prompt_tokens,
                        'completionTokens': completion_tokens,
                        'totalTokens': total_tokens
                    },
                    'type': 'token'
                }

                yield f"data: {json.dumps(bot_data)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
