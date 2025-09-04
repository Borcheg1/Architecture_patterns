import datetime

import pytest
from pytest_factoryboy import register

from src.tests.unit.factories import BatchFactory, OrderLineFactory, ProductFactory

register(ProductFactory, "product")
register(BatchFactory, "batch")
register(OrderLineFactory, "order_line")


@pytest.fixture()
def empty_batch() -> Batch:
    return BatchFactory(quantity=0)


@pytest.fixture()
def old_batch() -> Batch:
    return BatchFactory(eta=datetime.datetime(year=2020, month=1, day=1))
