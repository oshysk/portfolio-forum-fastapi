"""
掲示板に関するAPIを定義するモジュール。
"""

from fastapi import APIRouter, status, Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.schemas import common as common_schema
from src.schemas import error as error_schema
from src.schemas import forum as forum_schema
from src.cruds import forum as forum_crud

router = APIRouter()


@router.get(
    "/forums",
    summary="掲示板一覧取得",
    description="掲示板の一覧を取得する。",
    tags=["掲示板"],
    status_code=status.HTTP_200_OK,
)
async def get_forums(
    database_session: AsyncSession = Depends(get_session),
) -> forum_schema.Forums:
    schema: forum_schema.Forums = await forum_crud.get_forums(database_session)
    return schema


@router.post(
    "/forums",
    summary="掲示板作成",
    description="掲示板を作成する。",
    tags=["掲示板"],
    status_code=status.HTTP_201_CREATED,
)
async def create_forum(
    body: forum_schema.ForumCreate,
    database_session: AsyncSession = Depends(get_session),
) -> forum_schema.Forum:
    schema: forum_schema.Forum = await forum_crud.create_forum(
        session=database_session,
        forum_create=body,
    )
    return schema


@router.get(
    "/forums/{forum_id}",
    summary="掲示板取得",
    description="掲示板を取得する。",
    tags=["掲示板"],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": error_schema.ErrorMessage}},
)
async def get_forum(
    forum_id: int = Path(..., description="掲示板ID"),
    database_session: AsyncSession = Depends(get_session),
) -> forum_schema.Forum:
    # データベースから取得する。
    schema: forum_schema.Forum | None = await forum_crud.get_forum(
        session=database_session,
        forum_id=forum_id,
    )
    # 取得件数が0件の場合は404を返却する。
    if schema is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="掲示板が見つかりません。",
        )
    # 取得結果を返却する。
    return schema


@router.put(
    "/forums/{forum_id}",
    summary="掲示板編集",
    description="掲示板を編集する。",
    tags=["掲示板"],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": error_schema.ErrorMessage}},
)
async def edit_forum(
    body: forum_schema.ForumCreate,
    forum_id: int = Path(..., description="掲示板ID"),
    database_session: AsyncSession = Depends(get_session),
) -> forum_schema.Forum:
    # データベースを更新する。
    schema: forum_schema.Forum | None = await forum_crud.edit_forum(
        session=database_session,
        forum_id=forum_id,
        forum_create=body,
    )
    # 掲示板が見つからない場合は404を返却する。
    if schema is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="掲示板が見つかりません。",
        )
    # 200を返却する。
    return schema


@router.delete(
    "/forums/{forum_id}",
    summary="掲示板削除",
    description="掲示板を削除する。",
    tags=["掲示板"],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": error_schema.ErrorMessage}},
)
async def delete_forum(
    forum_id: int = Path(..., description="掲示板ID"),
    database_session: AsyncSession = Depends(get_session),
) -> common_schema.NoData:
    # データベースを削除する。
    schema: common_schema.NoData | None = await forum_crud.delete_forum(
        session=database_session,
        forum_id=forum_id,
    )
    # 掲示板が見つからない場合は404を返却する。
    if schema is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="掲示板が見つかりません。",
        )
    # 200を返却する。
    return schema
