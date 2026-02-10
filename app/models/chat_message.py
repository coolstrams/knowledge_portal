from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, BigInteger, String, DateTime, Text, Boolean, Index


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_message"

    # 数据库主键
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column(BigInteger, autoincrement=True)
    )

    # 业务字段
    user_id: str = Field(
        sa_column=Column(String(64), nullable=False, index=True),
        description="用户ID"
    )

    conversation_id: str = Field(
        sa_column=Column(String(64), nullable=False, index=True),
        description="会话ID"
    )

    message_id: str = Field(
        sa_column=Column(String(64), nullable=False, unique=True),
        description="消息业务ID（yyyymmddHHMMSS+uuid16）"
    )

    is_bot: bool = Field(
        sa_column=Column(Boolean, nullable=False),
        description="是否为机器人消息"
    )

    type: str = Field(
        sa_column=Column(String(32), nullable=False),
        description="消息类型（question / answer / system）"
    )

    category: Optional[str] = Field(
        default=None,
        sa_column=Column(String(64)),
        description="业务分类"
    )

    content: str = Field(
        sa_column=Column(Text, nullable=False),
        description="消息内容"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
        description="创建时间"
    )


# 👉 推荐索引（非常重要）
Index("idx_chat_message_conv_time", ChatMessage.conversation_id, ChatMessage.created_at)
Index("idx_chat_message_user_time", ChatMessage.user_id, ChatMessage.created_at)
