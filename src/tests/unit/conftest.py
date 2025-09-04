import pytest
from pytest_factoryboy import register

from src.tests.unit.factories import ProductFactory, BatchFactory, OrderLineFactory

register(ProductFactory)
register(BatchFactory, "batch")
register(OrderLineFactory, "order_line")


@pytest.fixture()
def empty_batch() -> Batch:
    return BatchFactory(quantity=0)
