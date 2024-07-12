"""
掲示板削除
DELETE:/forums/{forum_id}
"""

from datetime import datetime
import pytest
from httpx import AsyncClient, Response
from starlette import status


@pytest.mark.asyncio
async def test_delete_forum(async_client: AsyncClient) -> None:
    """
    掲示板を削除するテスト
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

    async def delete_forum_and_check() -> None:
        """
        掲示板を削除して確認する。
        """
        forum_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}"
        response: Response = await async_client.delete(endpoint)
        assert response.status_code == status.HTTP_200_OK
        return None

    await create_forum()
    await delete_forum_and_check()
    return None


@pytest.mark.asyncio
async def test_response_code_404(async_client: AsyncClient) -> None:
    """
    ResponseCode404を確認するテスト
    """
    not_exist_forum_id: int = 1
    endpoint: str = f"/forums/{str(not_exist_forum_id)}"
    response: Response = await async_client.delete(endpoint)
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
