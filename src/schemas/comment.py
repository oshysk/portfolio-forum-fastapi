"""
掲示板コメントに関するスキーマを定義するモジュール。
"""

import datetime
from pydantic import BaseModel, Field, ConfigDict


class CommentCreate(BaseModel):
    """
    コメント作成用
    """

    comment: str = Field(
        description="コメント",
        examples=["コメント"],
        max_length=100,
    )


class Comment(CommentCreate):
    """
    コメント取得用
    """

    forum_id: int = Field(
        description="掲示板ID",
        examples=[1],
    )

    comment_id: int = Field(
        description="コメントID",
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


class Comments(BaseModel):
    """
    コメント一覧取得用
    """

    comments: list[Comment] = Field(
        description="コメントの一覧",
        default=Comment,
    )
