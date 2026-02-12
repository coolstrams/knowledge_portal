from typing import Optional, List
from datetime import datetime

from sqlmodel import SQLModel, Field, Integer, select, update
from sqlalchemy import Column, BigInteger, String, DateTime, Text, Boolean, Index
from app.db.base import session_getter


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_message"

    # 数据库主键
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
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

    is_deleted: int = Field(
        default=0,
        sa_column=Column(Integer, nullable=False),
        description="是否删除"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
        description="创建时间"
    )


# 👉 推荐索引（非常重要）
Index("idx_chat_message_conv_time", "conversation_id", "created_at")
Index("idx_chat_message_user_time", "user_id", "created_at")


class ChatMessageDao(ChatMessage):
    @classmethod
    def create_message(cls, message_info: ChatMessage) -> ChatMessage:
        with session_getter() as session:
            message = cls(
                user_id=message_info.user_id,
                conversation_id=message_info.conversation_id,
                message_id=message_info.message_id,
                is_bot=message_info.is_bot,
                type=message_info.type,
                category=message_info.category,
                content=message_info.content,
                is_deleted=0
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message

    @classmethod
    def delete_message(cls, message_info: ChatMessage) -> ChatMessage:
        with session_getter() as session:
            session.delete(message_info)
            session.commit()
            return message_info

    @classmethod
    def get_message_by_conversation_id(cls, conversation_id: int) -> List[ChatMessage]:
        with session_getter() as session:
            statement = select(ChatMessage).where(ChatMessage.conversation_id == conversation_id)
            return session.exec(statement).all()
