from typing import Optional, List
from datetime import datetime

from sqlmodel import SQLModel, Field, select, update
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Index
from app.models.base import SQLModelSerializable
from app.db.base import session_getter


class ChatConversation(SQLModelSerializable, table=True):
    __tablename__ = "chat_conversation"

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


# 👉 推荐索引
Index("idx_chat_conversation_user_time", "user_id", "created_at")


class ChatConversationDao(ChatConversation):
    @classmethod
    def create_conversation(cls, conversation_info: ChatConversation) -> ChatConversation:
        with session_getter() as session:
            conversation = cls(
                user_id=conversation_info.user_id,
                conversation_id=conversation_info.conversation_id,
                type=conversation_info.type,
                category=conversation_info.category,
                title=conversation_info.title,
                is_deleted=0
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation

    @classmethod
    def delete_conversation(cls, conversation_info: ChatConversation) -> ChatConversation:
        with session_getter() as session:
            session.delete(conversation_info)
            session.commit()
            return conversation_info

    @classmethod
    def get_conversation_by_user(cls, user_id: int) -> List[ChatConversation]:
        with session_getter() as session:
            statement = select(ChatConversation).where(ChatConversation.user_id == user_id)
            return session.exec(statement).all()
