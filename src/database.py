from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

ASYNC_DB_URL = "mysql+aiomysql://root@database:3306/forum?charset=utf8"

async_engine: AsyncEngine = create_async_engine(ASYNC_DB_URL, echo=True)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,  # type: ignore
    class_=AsyncSession,
)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:  # type: ignore
        session: AsyncSession
        yield session
