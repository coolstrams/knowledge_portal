from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, BigInteger, String, DateTime, Index


class ChatConversation(SQLModel, table=True):
    __tablename__ = "chat_conversation"

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
        sa_column=Column(String(64), nullable=False, unique=True),
        description="会话业务ID（yyyymmddHHMMSS+uuid16）"
    )

    type: str = Field(
        sa_column=Column(String(32), nullable=False),
        description="会话类型（chat / rag / agent 等）"
    )

    category: Optional[str] = Field(
        default=None,
        sa_column=Column(String(64)),
        description="业务分类"
    )

    title: Optional[str] = Field(
        default=None,
        sa_column=Column(String(255)),
        description="会话标题"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
        description="创建时间"
    )


# 👉 推荐索引
Index("idx_chat_conversation_user_time", ChatConversation.user_id, ChatConversation.created_at)
