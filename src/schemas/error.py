"""
エラーに関するスキーマを定義するモジュール。
"""

from typing import Any
from pydantic import BaseModel, Field


class ErrorMessage(BaseModel):
    """
    エラーメッセージ
    """

    detail: str = Field(
        description="エラーメッセージ",
        examples=["情報が見つかりませんでした。"],
    )


class ValidationError(BaseModel):
    """
    バリデーションエラーメッセージ
    """

    type: Any = Field(
        description="バリデーションエラーの識別子",
        examples=["missing"],
    )
    loc: Any = Field(
        description="バリデーションエラーの発生場所",
        examples=[{"body", "password"}],
    )
    msg: Any = Field(
        description="バリデーションエラーのメッセージ",
        examples=["Field required"],
    )


class ValidationErrors(BaseModel):
    """
    バリデーションエラーメッセージ一覧
    """

    detail: list[ValidationError] = Field(
        description="バリデーションエラーメッセージの一覧",
        default=ValidationError,
    )
