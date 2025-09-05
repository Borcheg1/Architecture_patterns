import datetime
import random

from pytest_factoryboy import register

from src.models.allocate_dto import Batch, OrderLine, Product
from src.tests.unit.factories import OrderLineFactory, ProductFactory

register(ProductFactory, "product")
register(OrderLineFactory, "order_line")


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
