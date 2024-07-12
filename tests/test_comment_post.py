"""
掲示板コメント作成
POST:/forums/{forum_id}/comments
"""

from datetime import datetime
import pytest
from httpx import AsyncClient, Response
from starlette import status


@pytest.mark.asyncio
async def test_create_three_comments(async_client: AsyncClient) -> None:
    """
    3件の掲示板コメントを作成するテスト
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

    async def create_three_comments_and_check() -> None:
        """
        3件の掲示板コメントを作成して確認する。
        """
        forum_id: int = 1
        endpoint: str = f"/forums/{str(forum_id)}/comments"
        comment_ids: list[int] = [1, 2, 3]
        for end_string in ["first", "second", "third"]:
            request_body: dict = {
                "comment": f"comment_value_{end_string}",
            }
            response: Response = await async_client.post(
                endpoint,
                json=request_body,
            )
            assert response.status_code == status.HTTP_201_CREATED
            response_body: dict = response.json()
            assert response_body["comment"] == f"comment_value_{end_string}"
            assert response_body["forum_id"] == 1
            assert response_body["comment_id"] in comment_ids
            comment_ids.remove(response_body["comment_id"])
            # 日付変換はassert未使用だが失敗したら例外が発生する。
            datetime.strptime(response_body["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            datetime.strptime(response_body["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
        assert len(comment_ids) == 0
        return None

    await create_forum()
    await create_three_comments_and_check()
    return None


@pytest.mark.asyncio
async def test_response_code_404(async_client: AsyncClient) -> None:
    """
    ResponseCode404を確認するテスト
    """
    not_exist_forum_id: int = 100
    endpoint: str = f"/forums/{str(not_exist_forum_id)}/comments"
    request_body: dict = {
        "comment": "comment_value",
    }
    response: Response = await async_client.post(endpoint, json=request_body)
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
    endpoint: str = f"/forums/{str(forum_id)}/comments"
    request_body: dict = {
        # "comment": "comment_value",
    }
    response: Response = await async_client.post(endpoint, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_body: dict = response.json()
    assert "detail" in response_body
    for detail in response_body["detail"]:
        assert "type" in detail
        assert "loc" in detail
        assert "msg" in detail
    return None
