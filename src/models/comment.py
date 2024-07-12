"""
掲示板のモデルを定義するモジュール。
"""

import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class Comment(Base):
    """
    コメントモデル
    """

    __tablename__ = "Comment"

    # カラム定義
    forum_id = Column(
        "forum_id",
        Integer,
        ForeignKey("forum.forum_id"),
        primary_key=True,
    )
    comment_id = Column(
        Integer,
        primary_key=True,
    )
    comment = Column(
        "comment",
        String(100),
        nullable=False,
    )
    created_at = Column(
        "created_at",
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    # リレーション定義
    forum = relationship(
        "Forum",
        back_populates="comment",
    )
