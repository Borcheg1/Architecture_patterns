# stdlib
from collections.abc import AsyncGenerator, Generator

# thirdparty
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

# project
from src.core.config import settings
from src.models.orm_models import metadata, start_mappers


@pytest_asyncio.fixture(scope="session")
def async_engine() -> Generator:
    test_engine = create_async_engine(settings.test_database_path, echo=settings.echo_queries, future=True)
    start_mappers()
    yield test_engine
    test_engine.sync_engine.dispose()


@pytest_asyncio.fixture
async def prepare_tables(async_engine: AsyncEngine) -> AsyncGenerator:
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture
async def session(async_engine: AsyncEngine, prepare_tables: AsyncGenerator) -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session
