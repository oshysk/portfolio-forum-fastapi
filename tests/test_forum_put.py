"""
掲示板編集
GET:/forums/{forum_id}
"""

from datetime import datetime
import pytest
from httpx import AsyncClient, Response
from starlette import status


@pytest.mark.asyncio
async def test_edit_forum(async_client: AsyncClient) -> None:
    """
    掲示板を編集するテスト
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

    async def edit_forum_and_check() -> None:
        """
        掲示板を編集して確認する。
        """
        request_body: dict = {
            "title": "title_value_edit",
            "content": "content_value_edit",
        }
        forum_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}"
        response: Response = await async_client.put(endpoint, json=request_body)
        assert response.status_code == status.HTTP_200_OK
        response_body: dict = response.json()
        assert response_body["title"] == "title_value_edit"
        assert response_body["content"] == "content_value_edit"
        assert response_body["forum_id"] == 1
        # 日付変換はassert未使用だが失敗したら例外が発生する。
        datetime.strptime(response_body["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        datetime.strptime(response_body["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
        return None

    await create_forum()
    await edit_forum_and_check()
    return None


@pytest.mark.asyncio
async def test_response_code_404(async_client: AsyncClient) -> None:
    """
    ResponseCode404を確認するテスト
    """
    request_body: dict = {
        "title": "title_value",
        "content": "content_value",
    }
    not_exist_forum_id: int = 1
    endpoint: str = f"/forums/{str(not_exist_forum_id)}"
    response: Response = await async_client.put(
        endpoint,
        json=request_body,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_body: dict = response.json()
    assert "detail" in response_body
    return None


@pytest.mark.asyncio
async def test_response_code_422(async_client: AsyncClient) -> None:
    """
    ResponseCode422を確認するテスト
    """
    request_body: dict = {
        "title": "title_value_edit",
        # "content": "content_value_edit",
    }
    forum_id: int = 1
    target_url: str = f"/forums/{str(forum_id)}"
    response: Response = await async_client.put(target_url, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_body: dict = response.json()
    assert "detail" in response_body
    for detail in response_body["detail"]:
        assert "type" in detail
        assert "loc" in detail
        assert "msg" in detail
    return None
