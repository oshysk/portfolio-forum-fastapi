"""
掲示板コメントに対するCRUD操作を行うモジュール。
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models import forum as forum_model
from src.models import comment as comment_model
from src.schemas import common as common_schema
from src.schemas import forum as comment_schema
from src.schemas import comment as comment_schema


async def get_comments(
    session: AsyncSession,
    forum_id: int,
) -> comment_schema.Comments:
    """
    コメント一覧を取得する。
    """
    Model = comment_model.Comment
    # レコードを取得する。
    database_result = await session.execute(
        select(Model).where(Model.forum_id == forum_id)
    )
    rows = database_result.scalars().all()
    # 返却オブジェクトを作成して返却する。
    schema = comment_schema.Comments(comments=list())
    for row in rows:
        comment = comment_schema.Comment(
            forum_id=row.forum_id,  # type: ignore
            comment_id=row.comment_id,  # type: ignore
            comment=str(row.comment),
            created_at=row.created_at,  # type: ignore
            updated_at=row.updated_at,  # type: ignore
        )
        schema.comments.append(comment)
    return schema


async def create_comment(
    session: AsyncSession,
    forum_id: int,
    forum_comment: comment_schema.CommentCreate,
) -> comment_schema.Comment:
    """
    コメントを作成する。
    """
    Model = comment_model.Comment
    # comment_idを作成する。
    database_result = await session.execute(
        select(func.max(Model.comment_id)).where(Model.forum_id == forum_id),
    )
    comment_id: int | None = database_result.scalar_one_or_none()
    if comment_id is None:
        comment_id = 1
    else:
        comment_id += 1
    # レコードを作成する。
    row: comment_model.Comment = comment_model.Comment(
        forum_id=forum_id,
        comment_id=comment_id,
        **forum_comment.model_dump(),
    )
    session.add(row)
    await session.commit()
    # 最新レコードを取得して返却する。
    await session.refresh(row)
    schema: comment_schema.Comment = comment_schema.Comment(
        forum_id=row.forum_id,  # type: ignore
        comment_id=row.comment_id,  # type: ignore
        comment=str(row.comment),
        created_at=row.created_at,  # type: ignore
        updated_at=row.updated_at,  # type: ignore
    )
    return schema


async def get_comment(
    session: AsyncSession,
    forum_id: int,
    comment_id: int,
) -> comment_schema.Comment | None:
    """
    掲示板コメントを取得する。
    掲示板コメントが存在しない場合はNoneを返却する。
    """
    Model = comment_model.Comment
    # レコードを取得する。
    database_result = await session.execute(
        select(Model).filter(
            Model.forum_id == forum_id,
            Model.comment_id == comment_id,
        )
    )
    row = database_result.scalar_one_or_none()
    # 取得対象のレコードが存在しない場合はNoneを返却する。
    if row is None:
        return None
    # 返却オブジェクトを作成して返却する。
    schema = comment_schema.Comment(
        forum_id=row.forum_id,  # type: ignore
        comment_id=row.comment_id,  # type: ignore
        comment=row.comment,  # type: ignore
        created_at=row.created_at,  # type: ignore
        updated_at=row.updated_at,  # type: ignore
    )
    return schema


async def edit_comment(
    session: AsyncSession,
    forum_id: int,
    comment_id: int,
    comment_create: comment_schema.CommentCreate,
) -> comment_schema.Comment | None:
    """
    掲示板コメントを更新する。
    掲示板コメントが存在しない場合はNoneを返却する。
    """
    Model = comment_model.Comment
    # 更新対象のレコードを取得する。
    result = await session.execute(
        select(Model).where(
            Model.forum_id == forum_id,
            Model.comment_id == comment_id,
        ),
    )
    row: comment_model.Comment | None = result.scalar_one_or_none()
    # 更新対象のレコードが存在しない場合はNoneを返却する。
    if row is None:
        return None
    # 更新を実行する。
    row.comment = comment_create.comment  # type: ignore
    await session.commit()
    await session.refresh(row)
    # 返却オブジェクトを作成して返却する。
    schema = comment_schema.Comment(
        forum_id=row.forum_id,  # type: ignore
        comment_id=row.comment_id,  # type: ignore
        comment=str(row.comment),
        created_at=row.created_at,  # type: ignore
        updated_at=row.updated_at,  # type: ignore
    )
    return schema


async def delete_comment(
    session: AsyncSession,
    forum_id: int,
    comment_id: int,
) -> common_schema.NoData | None:
    """
    掲示板コメントを削除する。
    掲示板コメントが存在しない場合はNoneを返却する。
    """
    Model = comment_model.Comment
    # 削除対象のレコードを取得する。
    result = await session.execute(
        select(Model).where(
            Model.forum_id == forum_id,
            Model.comment_id == comment_id,
        ),
    )
    row: comment_model.Comment | None = result.scalar_one_or_none()
    # 更新対象のレコードが存在しない場合はNoneを返却する。
    if row is None:
        return None
    # 削除を実行してNoDataを返却する。
    await session.delete(row)
    await session.commit()
    return common_schema.NoData()
