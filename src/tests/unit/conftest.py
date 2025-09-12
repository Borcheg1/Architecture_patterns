# thirdparty
import pytest

# project
from src.models.domain_models import Batch, OrderLine, Product


@pytest.fixture
def order_line() -> OrderLine:
    return OrderLine("order1", Product("SOME-PRODUCT"), quantity=10)


@pytest.fixture
def batch() -> Batch:
    return Batch(ref="batch1", product=Product("SOME-PRODUCT"), quantity=50, eta=None)
