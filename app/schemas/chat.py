from typing import List, Optional, Literal
from pydantic import BaseModel


class ChatMessageItem(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    modelID: str = "qwen-plus" | None
    stream: bool = True | None
    messages: list[ChatMessageItem] | [{"role": "user", "content": "hello"}]
    enableThinking: bool = True | None
    conversationID: str | ""
    parentMessageID: str | ""
    session_id: str
    query: str
