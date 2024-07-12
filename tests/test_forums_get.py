"""
掲示板一覧取得
GET:/forums
"""

from datetime import datetime
import pytest
from httpx import AsyncClient, Response
from starlette import status


@pytest.mark.asyncio
async def test_get_zero_forum(async_client: AsyncClient) -> None:
    """
    0件の掲示板を取得するテスト
    """
    response: Response = await async_client.get("/forums")
    assert response.status_code == status.HTTP_200_OK
    response_body: dict = response.json()
    assert len(response_body["forums"]) == 0
    return None


@pytest.mark.asyncio
async def test_get_three_forums(async_client: AsyncClient) -> None:
    """
    3件の掲示板を取得するテスト
    """

    async def create_three_forums() -> None:
        """
        3件の掲示板を作成する。
        """
        request_body: dict = {
            "title": "title_value",
            "content": "content_value",
        }
        for _ in range(3):
            await async_client.post(
                "/forums",
                json=request_body,
            )
        return None

    async def get_three_forums_and_check() -> None:
        """
        3件の掲示板を取得して確認する。
        """
        response: Response = await async_client.get("/forums")
        assert response.status_code == status.HTTP_200_OK
        response_body: dict = response.json()
        forums: list[dict] = response_body["forums"]
        assert len(forums) == 3
        forum_ids: list[int] = [1, 2, 3]
        for forum in forums:
            assert forum["title"] == "title_value"
            assert forum["content"] == "content_value"
            assert forum["forum_id"] in forum_ids
            forum_ids.remove(forum["forum_id"])
            # 日付変換はassert未使用だが失敗したら例外が発生する。
            datetime.strptime(forum["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            datetime.strptime(forum["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
        assert len(forum_ids) == 0
        return None

    await create_three_forums()
    await get_three_forums_and_check()
    return None
