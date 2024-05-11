from typing import Optional
from sqlmodel import Field, SQLModel
from orm.database import engine
from func import get_uid, get_cid
from func import get_bid,get_nickname
import time


class User(SQLModel, table=True):
    __tablename__ = 'User'
    uid: Optional[int] = Field(default_factory=get_uid, primary_key=True)
    name: str = Field(unique=True)
    nickname: Optional[str] = Field(default_factory=get_nickname, unique=True)
    email: str
    hashed_password: str
    salt: str
    admin: Optional[bool] = Field(default=False)
    avatar: Optional[str] = Field(default=None, nullable=True)
    created_at: Optional[int] = Field(default_factory=lambda: int(time.time()))


class Blog(SQLModel, table=True):
    __tablename__ = 'Blog'
    bid: Optional[int] = Field(default_factory=get_bid, primary_key=True)
    user_id: int = Field(foreign_key="User.uid")
    title: str
    summary: str
    content_path: str
    created_at: Optional[int] = Field(default_factory=lambda: int(time.time()))
    last_modified_at: Optional[int] = Field(default=None, nullable=True)


class Comment(SQLModel, table=True):
    __tablename__ = 'Comment'
    cid: Optional[int] = Field(default_factory=get_cid, primary_key=True)
    blog_id: int = Field(foreign_key="Blog.bid")
    user_id: int = Field(foreign_key="User.uid")
    content: str
    created_at: Optional[int] = Field(default_factory=lambda: int(time.time()))
