"""
掲示板作成
POST:/forums
"""

from datetime import datetime
import pytest
from httpx import AsyncClient, Response
from starlette import status


@pytest.mark.asyncio
async def test_create_one_forum(async_client: AsyncClient) -> None:
    """
    1件の掲示板を作成するテスト
    """
    request_body: dict = {
        "title": "title_value_first",
        "content": "content_value_first",
    }
    response: Response = await async_client.post(
        "/forums",
        json=request_body,
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_body: dict = response.json()
    assert response_body["title"] == "title_value_first"
    assert response_body["content"] == "content_value_first"
    assert response_body["forum_id"] == 1
    # 日付変換はassert未使用だが失敗したら例外が発生する。
    datetime.strptime(response_body["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
    datetime.strptime(response_body["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
    return None


@pytest.mark.asyncio
async def test_create_three_forums(async_client: AsyncClient) -> None:
    """
    3件の掲示板を作成するテスト
    """

    forum_ids: list[int] = [1, 2, 3]
    for end_string in ["first", "second", "third"]:
        request_body: dict = {
            "title": f"title_value_{end_string}",
            "content": f"content_value_{end_string}",
        }
        response: Response = await async_client.post(
            "/forums",
            json=request_body,
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_body: dict = response.json()
        assert response_body["title"] == f"title_value_{end_string}"
        assert response_body["content"] == f"content_value_{end_string}"
        forum_ids.remove(response_body["forum_id"])
        # 日付変換はassert未使用だが失敗したら例外が発生する。
        datetime.strptime(response_body["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        datetime.strptime(response_body["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
    assert len(forum_ids) == 0
    return None


@pytest.mark.asyncio
async def test_response_code_422(async_client: AsyncClient) -> None:
    """
    ResponseCode422を確認するテスト
    """

    request_body: dict = {
        "title": "title_value_second",
        # "content": "content_value_second",
    }
    response: Response = await async_client.post(
        "/forums",
        json=request_body,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_body: dict = response.json()
    assert "detail" in response_body
    for detail in response_body["detail"]:
        assert "type" in detail
        assert "loc" in detail
        assert "msg" in detail
    return None
