# stdlib
import datetime

# thirdparty
import pytest

# project
from src.models.domain_models import Batch, OrderLine, Product


@pytest.fixture
def order_line(quantity: int = 10) -> OrderLine:
    return OrderLine("order1", Product("SOME-PRODUCT"), quantity=quantity)


@pytest.fixture
def batch(reference: str, quantity: int = 50, eta: datetime.datetime | None = None) -> Batch:
    return Batch(ref=reference, product=Product("SOME-PRODUCT"), quantity=quantity, eta=eta)
