"""
掲示板コメント編集
PUT:/forums/{forum_id}/comments/{comment_id}
"""

from datetime import datetime
import pytest
from httpx import AsyncClient, Response
from starlette import status


@pytest.mark.asyncio
async def test_edit_comment(async_client: AsyncClient) -> None:
    """
    掲示板コメントを編集するテスト
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
        掲示板コメントを作成する。
        """
        forum_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}/comments"
        request_body: dict = {
            "comment": "comment_value",
        }
        await async_client.post(endpoint, json=request_body)
        return None

    async def edit_comment_and_check() -> None:
        """
        掲示板コメントを編集して確認する。
        """
        forum_id: int = 1
        comment_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}/comments/{comment_id}"
        request_body: dict = {
            "comment": "comment_value_edit",
        }
        response: Response = await async_client.put(endpoint, json=request_body)
        assert response.status_code == status.HTTP_200_OK
        response_body: dict = response.json()
        assert response_body["comment"] == "comment_value_edit"
        assert response_body["forum_id"] == 1
        assert response_body["comment_id"] == 1
        # 日付変換はassert未使用だが失敗したら例外が発生する。
        datetime.strptime(response_body["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        datetime.strptime(response_body["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
        return None

    await create_forum()
    await create_three_comments()
    await edit_comment_and_check()
    return None


@pytest.mark.asyncio
async def test_response_code_404(async_client: AsyncClient) -> None:
    """
    ResponseCode404を確認するテスト
    """
    not_exist_forum_id: int = 100
    not_exist_comment_id: int = 100
    endpoint: str = f"/forums/{str(not_exist_forum_id)}/{not_exist_comment_id}"
    request_body: dict = {
        "comment": "comment_value_edit",
    }
    response: Response = await async_client.put(endpoint, json=request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_body: dict = response.json()
    assert "detail" in response_body
    return None


@pytest.mark.asyncio
async def test_response_code_422(async_client: AsyncClient) -> None:
    """
    ResponseCode422を確認するテスト
    """
    forum_id: int = 1
    comment_id: int = 1
    endpoint: str = f"/forums/{str(forum_id)}/comments/{str(comment_id)}"
    request_body: dict = {
        # "comment": "comment_value",
    }
    response: Response = await async_client.put(endpoint, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_body: dict = response.json()
    assert "detail" in response_body
    for detail in response_body["detail"]:
        assert "type" in detail
        assert "loc" in detail
        assert "msg" in detail
    return None
