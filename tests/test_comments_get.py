"""
掲示板コメント取得
GET:/forums/{forum_id}/comments
"""

from datetime import datetime
import pytest
from httpx import AsyncClient, Response
from starlette import status


@pytest.mark.asyncio
async def test_get_zero_comment(async_client: AsyncClient) -> None:
    """
    0件の掲示板コメントを取得するテスト
    """

    async def create_forum() -> None:
        """
        掲示板を作成する。
        """
        request_body: dict = {
            "title": "title_value",
            "content": "content_value",
        }
        await async_client.post(
            "/forums",
            json=request_body,
        )
        return None

    async def get_comments_and_check() -> None:
        """
        掲示板コメントを取得して確認する。
        """
        forum_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}/comments"
        response: Response = await async_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK
        response_body: dict = response.json()
        assert len(response_body["comments"]) == 0
        return None

    await create_forum()
    await get_comments_and_check()
    return None


@pytest.mark.asyncio
async def test_get_three_comments(async_client: AsyncClient) -> None:
    """
    3件のコメントを取得するテスト
    """

    async def create_forum() -> None:
        """
        掲示板を作成する。
        """
        request_body: dict = {
            "title": "title_value",
            "content": "content_value",
        }
        await async_client.post(
            "/forums",
            json=request_body,
        )
        return None

    async def create_three_comments() -> None:
        """
        3件の掲示板コメントを作成する。
        """
        forum_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}/comments"
        request_body: dict = {
            "comment": "comment_value",
        }
        for _ in range(3):
            await async_client.post(endpoint, json=request_body)
        return None

    async def get_three_comments_and_check() -> None:
        """
        3件の掲示板コメントを取得して確認する。
        """
        forum_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}/comments"
        response: Response = await async_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK
        response_body: dict = response.json()
        comments: list[dict] = response_body["comments"]
        assert len(comments) == 3
        comments_ids: list[int] = [1, 2, 3]
        for comment in comments:
            assert comment["comment"] == "comment_value"
            assert comment["forum_id"] == 1
            assert comment["comment_id"] in comments_ids
            comments_ids.remove(comment["comment_id"])
            # 日付変換はassert未使用だが失敗したら例外が発生する。
            datetime.strptime(comment["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            datetime.strptime(comment["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
        assert len(comments_ids) == 0
        return None

    await create_forum()
    await create_three_comments()
    await get_three_comments_and_check()
    return None


@pytest.mark.asyncio
async def test_response_code_404(async_client: AsyncClient) -> None:
    """
    ResponseCode404を確認するテスト
    """
    not_exist_forum_id: int = 100
    endpoint: str = f"/forums/{str(not_exist_forum_id)}/comments"
    response: Response = await async_client.get(endpoint)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_body: dict = response.json()
    assert "detail" in response_body
    return None


@pytest.mark.asyncio
async def test_response_code_422(async_client: AsyncClient) -> None:
    """
    ResponseCode422を確認するテスト
    """
    # bodyパラメータが存在しないためエラー確認不可能。
    return None
