# thirdparty
import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

# project
from src.models.domain_models import OrderLine, Product

pytestmark = pytest.mark.asyncio


async def test_orderline_mapper_can_load_lines(session: AsyncSession) -> None:
    products_stmt = """
        INSERT INTO products (title) VALUES ('RED-CHAIR'), ('RED-TABLE'), ('BLUE-LIPSTICK')
    """
    order_lines_stmt = """
        INSERT INTO order_lines (order_id, product_id, quantity) VALUES (1, 1, 12), (1, 2, 13), (2, 3, 14)
    """

    await session.execute(text(products_stmt))
    await session.execute(text(order_lines_stmt))

    expected = [
        OrderLine("1", Product("RED-CHAIR"), 12),
        OrderLine("1", Product("RED-TABLE"), 13),
        OrderLine("2", Product("BLUE-LIPSTICK"), 14),
    ]

    result = await session.execute(select(OrderLine).options(joinedload(OrderLine.product)))
    assert result.scalars().all() == expected


async def test_orderline_mapper_can_save_lines(session: AsyncSession) -> None:
    query = """
        SELECT o.order_id, p.title, o.quantity FROM "order_lines" AS o
        JOIN products AS p ON p.id = o.product_id
    """

    new_line = OrderLine("1", Product("DECORATIVE-WIDGET"), 12)
    session.add(new_line)
    await session.commit()

    result = await session.execute(text(query))
    rows = result.all()
    assert rows == [("1", "DECORATIVE-WIDGET", 12)]
