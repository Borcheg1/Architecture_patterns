# thirdparty
import pytest
from sqlalchemy import text

# fastapi
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# project
from src.models.domain_models import OrderLine, Product

pytestmark = pytest.mark.asyncio


async def test_orderline_mapper_can_load_lines(session: AsyncSession) -> None:
    await session.exec(text("INSERT INTO products (title) VALUES ('RED-CHAIR'),('RED-TABLE'),('BLUE-LIPSTICK')"))

    await session.exec(
        text("INSERT INTO order_lines (order_id, product_id, quantity) VALUES (1, 1, 12),(1, 2, 13),(2, 3, 14)")
    )
    expected = [
        OrderLine("1", Product("RED-CHAIR"), 12),
        OrderLine("1", Product("RED-TABLE"), 13),
        OrderLine("2", Product("BLUE-LIPSTICK"), 14),
    ]

    result = await session.exec(select(OrderLine))
    assert result.all() == expected


async def test_orderline_mapper_can_save_lines(session: AsyncSession) -> None:
    new_line = OrderLine("1", Product("DECORATIVE-WIDGET"), 12)
    session.add(new_line)
    await session.commit()

    rows = list(await session.exec(text('SELECT order_id, product_id, quantity FROM "order_lines"')))
    assert rows == [("1", 1, 12)]
