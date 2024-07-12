import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from src.database import get_session, Base
from src.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    # Async用のengineとsessionを作成
    async_engine: AsyncEngine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)  # type: ignore

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
        async with async_session() as session:  # type: ignore
            yield session

    app.dependency_overrides[get_session] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    transport = ASGITransport(app=app)  # type: ignore
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
