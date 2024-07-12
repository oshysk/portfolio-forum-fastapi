"""
掲示板に関するスキーマを定義するモジュール。
"""

import datetime
from pydantic import BaseModel, Field, ConfigDict


class ForumCreate(BaseModel):
    """
    掲示板作成用
    """

    title: str = Field(
        description="タイトル",
        examples=["掲示板タイトル"],
        max_length=20,
    )
    content: str = Field(
        description="内容",
        examples=["掲示板の内容"],
        max_length=100,
    )


class Forum(ForumCreate):
    """
    掲示板取得用
    """

    forum_id: int = Field(
        description="掲示板ID",
        examples=[1],
    )
    created_at: datetime.datetime = Field(
        description="作成日",
        examples=["2024-01-01T12:34:56"],
    )
    updated_at: datetime.datetime = Field(
        description="更新日",
        examples=["2024-01-01T12:34:56"],
    )

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)


class Forums(BaseModel):
    """
    掲示板一覧取得用
    """

    forums: list[Forum] = Field(
        description="掲示板の一覧",
        default=Forum,
    )
