# thirdparty
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession

# project
from src.models.domain_models import Batch, OrderLine, Product
from src.repository.repository import SqlAlchemyRepository

pytestmark = pytest.mark.asyncio


async def insert_order_line(session: AsyncSession) -> int:
    products_stmt = """
        INSERT INTO products (title) VALUES ('GENERIC-SOFA')
    """
    order_lines_stmt = """
        INSERT INTO order_lines (order_id, product_id, quantity)
        VALUES ('order1', 1, 12)
    """
    order_lines_query = """
        SELECT o.id FROM order_lines AS o
        JOIN products AS p ON p.id = o.product_id
        WHERE o.order_id=:order_id AND p.title=:title
    """

    await session.execute(text(products_stmt))
    await session.execute(text(order_lines_stmt))
    queryset = await session.execute(text(order_lines_query).params(order_id="order1", title="GENERIC-SOFA"))

    return queryset.scalar_one()


async def insert_batch(session: AsyncSession, reference: str) -> int:
    product_stmt = """
        INSERT INTO products (title) VALUES ('GENERIC-SOFA')
    """
    batch_stmt = """
        INSERT INTO batches (reference, product_id, purchased_quantity, eta)
        VALUES (:reference, 1, 100, null)
    """
    batch_query = """
        SELECT b.id FROM batches AS b
        JOIN products AS p ON p.id = b.product_id
        WHERE b.reference=:reference
    """

    await session.execute(text(product_stmt))
    await session.execute(text(batch_stmt).params(reference=reference))
    queryset = await session.execute(text(batch_query).params(reference=reference))

    return queryset.scalar_one()


async def insert_allocation(session: AsyncSession, order_line_id: int, batch_id: int) -> int:
    allocation_stmt = """
        INSERT INTO allocations (order_line_id, batch_id)
        VALUES (:order_line_id, :batch_id)
    """
    allocation_query = """
        SELECT a.id FROM allocations AS a
        JOIN batches AS b ON b.id = a.batch_id
        JOIN order_lines AS o ON o.id = a.order_line_id
        WHERE b.id=:batch_id AND o.id=:order_line_id
    """

    await session.execute(text(allocation_stmt).params(order_line_id=order_line_id, batch_id=batch_id))
    queryset = await session.execute(text(allocation_query).params(batch_id=batch_id, order_line_id=order_line_id))

    return queryset.scalar_one()


async def test_repository_can_save_a_batch(session: AsyncSession) -> None:
    batch = Batch("batch1", Product("RUSTY-SOAPDISH"), 100, eta=None)
    query = """
        SELECT b.reference, p.title, b.purchased_quantity, b.eta FROM "batches" AS b
        JOIN "products" AS p ON p.id = b.product_id
    """

    repo = SqlAlchemyRepository(session)
    await repo.add(batch)
    await session.commit()

    rows = await session.execute(text(query))

    assert rows.all() == [("batch1", "RUSTY-SOAPDISH", 100, None)]


async def test_repository_can_retrieve_a_batch_with_allocations(session: AsyncSession) -> None:
    orderline_id = await insert_order_line(session)
    batch1_id = await insert_batch(session, "batch1")
    await insert_batch(session, "batch2")
    await insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = await repo.get("batch1")

    expected = Batch("batch1", Product("GENERIC-SOFA"), 100, eta=None)
    assert retrieved == expected
    assert retrieved.product.title == expected.product.title
    assert retrieved.purchased_quantity == expected.purchased_quantity
    assert retrieved.allocations == {OrderLine("order1", Product("GENERIC-SOFA"), 12)}
