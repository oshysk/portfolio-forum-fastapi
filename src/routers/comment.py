"""
掲示板コメントに関するAPIを定義するモジュール。
"""

from fastapi import APIRouter, status, Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.schemas import common as common_schema
from src.schemas import error as error_schema
from src.schemas import forum as forum_schema
from src.schemas import comment as comment_schema
from src.cruds import forum as forum_crud
from src.cruds import comment as comment_crud

router = APIRouter()


async def _return_404_if_board_not_exist(
    database_session: AsyncSession,
    forum_id: int,
) -> None:
    """
    掲示板が存在しない場合は404を返却する。
    """
    schema: forum_schema.Forum | None = await forum_crud.get_forum(
        session=database_session,
        forum_id=forum_id,
    )
    if schema is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="掲示板が見つかりません。",
        )
    return None


@router.get(
    "/forums/{forum_id}/comments",
    summary="掲示板コメント一覧取得",
    description="掲示板コメントの一覧を取得する。",
    tags=["掲示板コメント"],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": error_schema.ErrorMessage}},
)
async def get_comments(
    forum_id: int = Path(..., description="掲示板ID"),
    database_session: AsyncSession = Depends(get_session),
) -> comment_schema.Comments:
    # 掲示板が存在しない場合は404を返却する。
    await _return_404_if_board_not_exist(
        database_session=database_session,
        forum_id=forum_id,
    )
    # 掲示板コメント一覧を取得して返却する。
    schema: comment_schema.Comments = await comment_crud.get_comments(
        session=database_session,
        forum_id=forum_id,
    )
    return schema


@router.post(
    "/forums/{forum_id}/comments",
    summary="掲示板コメントを作成",
    description="掲示板コメントを作成する。",
    tags=["掲示板コメント"],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": common_schema.NoData},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": error_schema.ValidationErrors},
    },
)
async def create_comment(
    body: comment_schema.CommentCreate,
    forum_id: int = Path(..., description="掲示板ID"),
    database_session: AsyncSession = Depends(get_session),
) -> comment_schema.Comment:
    # 掲示板が存在しない場合は404を返却する。
    await _return_404_if_board_not_exist(
        database_session=database_session,
        forum_id=forum_id,
    )
    # 掲示板コメントを作成して返却する。
    schema: comment_schema.Comment = await comment_crud.create_comment(
        session=database_session,
        forum_id=forum_id,
        forum_comment=body,
    )
    return schema


@router.get(
    "/forums/{forum_id}/comments/{comment_id}",
    summary="掲示板コメントを取得",
    description="掲示板コメントを取得する。",
    tags=["掲示板コメント"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": common_schema.NoData},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": error_schema.ValidationErrors},
    },
)
async def get_comment(
    forum_id: int = Path(..., description="掲示板ID"),
    comment_id: int = Path(..., description="コメントID"),
    database_session: AsyncSession = Depends(get_session),
) -> comment_schema.Comment:
    # 掲示板が存在しない場合は404を返却する。
    await _return_404_if_board_not_exist(
        database_session=database_session,
        forum_id=forum_id,
    )
    # 掲示板コメントを取得する。
    shema: comment_schema.Comment | None = await comment_crud.get_comment(
        session=database_session,
        forum_id=forum_id,
        comment_id=comment_id,
    )
    # コメントが見つからない場合は404を返却する。
    if shema is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="掲示板コメントが見つかりません。",
        )
    # 200を返却する。
    return shema


@router.put(
    "/forums/{forum_id}/comments/{comment_id}",
    summary="掲示板コメント編集",
    description="掲示板コメントを編集する。",
    tags=["掲示板コメント"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": common_schema.NoData},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": error_schema.ValidationErrors},
    },
)
async def edit_comment(
    body: comment_schema.CommentCreate,
    forum_id: int = Path(..., description="掲示板ID"),
    comment_id: int = Path(..., description="コメントID"),
    database_session: AsyncSession = Depends(get_session),
) -> comment_schema.Comment:
    # 掲示板が存在しない場合は404を返却する。
    await _return_404_if_board_not_exist(
        database_session=database_session,
        forum_id=forum_id,
    )
    # データベースを更新する。
    schema: comment_schema.Comment | None = await comment_crud.edit_comment(
        session=database_session,
        forum_id=forum_id,
        comment_id=comment_id,
        comment_create=body,
    )
    # 掲示板が見つからない場合は404を返却する。
    if schema is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="掲示板コメントが見つかりません。",
        )
    # 200を返却する。
    return schema


@router.delete(
    "/forums/{forum_id}/comments/{comment_id}",
    summary="掲示板コメントを削除",
    description="掲示板コメントを削除する。",
    tags=["掲示板コメント"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": common_schema.NoData},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": error_schema.ValidationErrors},
    },
)
async def delete_comment(
    forum_id: int = Path(..., description="掲示板ID"),
    comment_id: int = Path(..., description="コメントID"),
    database_session: AsyncSession = Depends(get_session),
) -> common_schema.NoData:
    # 掲示板が存在しない場合は404を返却する。
    await _return_404_if_board_not_exist(
        database_session=database_session,
        forum_id=forum_id,
    )
    # データベースを削除する。
    schema: common_schema.NoData | None = await comment_crud.delete_comment(
        session=database_session,
        forum_id=forum_id,
        comment_id=comment_id,
    )
    # コメントが見つからない場合は404を返却する。
    if schema is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="掲示板コメントが見つかりません。",
        )
    # 200を返却する。
    return schema
