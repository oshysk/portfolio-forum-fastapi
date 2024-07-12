"""
共通で使用するスキーマを定義するモジュール。
"""

from pydantic import BaseModel


class NoData(BaseModel):
    """
    データ無し
    """

    pass
