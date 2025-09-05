# stdlib
from collections.abc import AsyncGenerator

# thirdparty
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# fastapi
from sqlmodel.ext.asyncio.session import AsyncSession

# project
from src.core.config import settings

engine = create_async_engine(settings.database_path, echo=settings.echo_queries, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
