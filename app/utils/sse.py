import json
from typing import Optional


def sse_json_event(
    *,
    token: str,
    conversation_id: str,
    session_id: str,
    message_id: str,
    parent_message_id: Optional[str] = ""
) -> str:
    payload = {
        "data": {
            "content": token
        },
        "meta": {
            "conversationID": conversation_id,
            "parentMessageID": parent_message_id,
            "messageID": message_id,
            "sessionID": session_id
        },
        "type": "answer"
    }

    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
