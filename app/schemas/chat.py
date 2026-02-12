from typing import List, Optional, Literal
from pydantic import BaseModel


class ChatMessageItem(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    modelID: str = "qwen-plus"
    stream: bool = True
    messages: list[ChatMessageItem]
    enableThinking: bool = True
    conversationID: str
    parentMessageID: str
    session_id: str
    query: str
