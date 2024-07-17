"""
掲示板のCRUD処理を行うモジュール。
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models import forum as forum_model
from src.schemas import common as common_schema
from src.schemas import forum as forum_schema


async def get_forums(
    session: AsyncSession,
) -> forum_schema.Forums:
    """
    掲示板一覧を取得する。
    """
    Model = forum_model.Forum
    # レコードを取得する。
    database_result = await session.execute(
        select(Model).order_by(Model.forum_id.desc())
    )
    rows = database_result.scalars().all()
    # 返却オブジェクトを作成して返却する。
    schema = forum_schema.Forums(forums=list())
    for row in rows:
        forum = forum_schema.Forum(
            title=str(row.title),
            content=str(row.content),
            forum_id=row.forum_id,  # type: ignore
            created_at=row.created_at,  # type: ignore
            updated_at=row.updated_at,  # type: ignore
        )
        schema.forums.append(forum)
    return schema


async def create_forum(
    session: AsyncSession,
    forum_create: forum_schema.ForumCreate,
) -> forum_schema.Forum:
    """
    掲示板を作成する。
    """
    # レコードを作成する。
    model = forum_model.Forum(**forum_create.model_dump())
    session.add(model)
    await session.commit()
    # 最新レコードを取得して返却する。
    await session.refresh(model)
    schema: forum_schema.Forum = forum_schema.Forum(
        title=str(model.title),
        content=str(model.content),
        forum_id=model.forum_id,  # type: ignore
        created_at=model.created_at,  # type: ignore
        updated_at=model.updated_at,  # type: ignore
    )
    return schema


async def get_forum(
    session: AsyncSession,
    forum_id: int,
) -> forum_schema.Forum | None:
    """
    掲示板を取得する。
    掲示板が存在しない場合はNoneを返却する。
    """
    Model = forum_model.Forum
    # レコードを取得する。
    database_result = await session.execute(
        select(Model).filter(Model.forum_id == forum_id)
    )
    row = database_result.scalar_one_or_none()
    # 取得対象のレコードが存在しない場合はNoneを返却する。
    if row is None:
        return None
    # 返却オブジェクトを作成して返却する。
    forum = forum_schema.Forum(
        title=str(row.title),
        content=str(row.content),
        forum_id=row.forum_id,  # type: ignore
        created_at=row.created_at,  # type: ignore
        updated_at=row.updated_at,  # type: ignore
    )
    return forum


async def edit_forum(
    session: AsyncSession,
    forum_id: int,
    forum_create: forum_schema.ForumCreate,
) -> forum_schema.Forum | None:
    """
    掲示板を更新する。
    掲示板が存在しない場合はNoneを返却する。
    """
    Model = forum_model.Forum
    # 更新対象のレコードを取得する。
    database_result = await session.execute(
        select(Model).where(Model.forum_id == forum_id),
    )
    row: forum_model.Forum | None = database_result.scalar_one_or_none()
    # 更新対象のレコードが存在しない場合はNoneを返却する。
    if row is None:
        return None
    # 更新を実行する。
    row.title = forum_create.title  # type: ignore
    row.content = forum_create.content  # type: ignore
    await session.commit()
    # 最新レコードを取得して返却する。
    await session.refresh(row)
    schema = forum_schema.Forum(
        title=str(row.title),
        content=str(row.content),
        forum_id=row.forum_id,  # type: ignore
        created_at=row.created_at,  # type: ignore
        updated_at=row.updated_at,  # type: ignore
    )
    return schema


async def delete_forum(
    session: AsyncSession,
    forum_id: int,
) -> common_schema.NoData | None:
    """
    掲示板を削除する。
    掲示板が存在しない場合はNoneを返却する。
    """
    Model = forum_model.Forum
    # 削除対象のレコードを取得する。
    database_result = await session.execute(
        select(Model).where(Model.forum_id == forum_id),
    )
    row: forum_model.Forum | None = database_result.scalar_one_or_none()
    # 削除対象のレコードが存在しない場合はNoneを返却する。
    if row is None:
        return None
    # 削除を実行してTrueを返却する。
    await session.delete(row)
    await session.commit()
    return common_schema.NoData()
