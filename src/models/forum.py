"""
掲示板のモデルを定義するモジュール。
"""

import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class Forum(Base):
    """
    掲示板モデル
    """

    __tablename__ = "forum"

    # カラム定義
    forum_id = Column(
        "forum_id",
        Integer,
        primary_key=True,
    )
    title = Column(
        "title",
        String(20),
        nullable=False,
    )
    content = Column(
        "content",
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
    comment = relationship(
        "Comment",
        back_populates="forum",
        cascade="delete",
    )
