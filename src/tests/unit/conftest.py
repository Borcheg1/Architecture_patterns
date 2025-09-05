# stdlib
import datetime
import random
from collections.abc import AsyncGenerator, Generator

# thirdparty
import pytest_asyncio
from pytest_factoryboy import register
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# fastapi
from sqlmodel.ext.asyncio.session import AsyncSession

# project
from src.core.config import settings
from src.models.domain_models import Batch, OrderLine, Product
from src.models.orm_models import metadata, start_mappers
from src.tests.unit.factories import OrderLineFactory, ProductFactory

register(ProductFactory, "product")
register(OrderLineFactory, "order_line")


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


def create_order_line_by_product(product: Product, quantity: int = 10) -> OrderLine:
    return OrderLineFactory.build(product=product, quantity=quantity)


def prepare_batch(
    product: Product,
    reference: str | None = None,
    quantity: int = 50,
    eta: datetime.datetime | None = None,
) -> Batch:
    if not reference:
        reference = str(random.randint(1, 100000))
    return Batch(ref=reference, product=product, quantity=quantity, eta=eta)
