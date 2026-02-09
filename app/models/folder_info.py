from typing import Optional

from sqlalchemy import Index, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlmodel import SQLModel, Field, Column
from models.base import SQLModelSerializable
from db.base import session_getter


class FolderInfoBase(SQLModelSerializable):
    folder_name: str = Field(
        sa_column=Column(VARCHAR(100), nullable=False, comment="文件夹名称")
    )
    parent_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, comment="父文件夹id")
    )
    create_user: Optional[str] = Field(
        default=None,
        sa_column=Column(VARCHAR(20), comment="创建用户")
    )
    create_time: Optional[str] = Field(
        default=None,
        sa_column=Column(VARCHAR(20), comment="创建时间，格式：yyyy-MM-dd hh:ss:mm")
    )
    ower_who: Optional[str] = Field(
        default=None,
        sa_column=Column(VARCHAR(1), comment="是否属于个人：1-属于个人，2-属于团队")
    )
    legal_personality: Optional[str] = Field(
        default=None,
        sa_column=Column(VARCHAR(100), comment="所属法人")
    )
    team_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            VARCHAR(45),
            comment="创建用户归属团队id，在ower_who是2时不能为空"
        )
    )
    user_space_id: Optional[str] = Field(
        default=None,
        sa_column=Column(VARCHAR(45), comment="创建用户归属空间id")
    )
    files_num: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, comment="文件夹下文件总数量")
    )
    llm_catalog_id: Optional[str] = Field(
        default=None,
        sa_column=Column(VARCHAR(45), comment="llm编目id")
    )


class FolderInfo(FolderInfoBase, table=True):
    __tablename__ = 'folder_info'
    __table_args__ = (
        Index('idx_create_user', 'create_user'),
        Index('idx_ower_who', 'ower_who'),
        Index('idx_parent_id', 'parent_id'),
        Index('idx_team_id', 'team_id'),
        {'comment': '文件夹目录信息表'}
    )

    id: int = Field(default=None, primary_key=True)


class FolderCreate(FolderInfoBase):
    create_user: str


class FolderInfoDao(FolderInfoBase):
    @classmethod
    def create_folder(cls, folder_info: FolderInfo, folder_name: str, create_user: str, parent_id: str = None):
        with session_getter as session:
            session.add(folder_info)
