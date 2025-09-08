# stdlib
from datetime import datetime, timedelta

# thirdparty
import pytest

# project
from src.exceptions.allocate import OutOfStock
from src.models.domain_models import Batch, OrderLine, Product, allocate

TODAY = datetime.today()
TOMORROW = TODAY + timedelta(days=1)
LATER = TOMORROW + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments(order_line: OrderLine) -> None:
    in_stock_batch = Batch(ref="batch1", product=Product("SOME-PRODUCT"), quantity=50)
    shipment_batch = Batch(ref="batch2", product=Product("SOME-PRODUCT"), quantity=50, eta=TOMORROW)
    order_line.quantity = 10

    allocate(order_line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 40
    assert shipment_batch.available_quantity == 50


def test_prefers_earlier_batches(order_line: OrderLine) -> None:
    earliest = Batch(ref="batch1", product=Product("SOME-PRODUCT"), quantity=50, eta=TODAY)
    medium = Batch(ref="batch2", product=Product("SOME-PRODUCT"), quantity=50, eta=TOMORROW)
    latest = Batch(ref="batch3", product=Product("SOME-PRODUCT"), quantity=50, eta=LATER)
    order_line.quantity = 10

    allocate(order_line, [medium, earliest, latest])

    assert earliest.available_quantity == 40
    assert medium.available_quantity == 50
    assert latest.available_quantity == 50


def test_returns_allocated_batch_ref(order_line: OrderLine) -> None:
    in_stock_batch = Batch(ref="batch1", product=Product("SOME-PRODUCT"), quantity=50)
    shipment_batch = Batch(ref="batch1", product=Product("SOME-PRODUCT"), quantity=50, eta=TOMORROW)
    order_line.quantity = 10

    allocation = allocate(order_line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate(order_line: OrderLine) -> None:
    batch = Batch(ref="batch1", product=Product("SOME-PRODUCT"), quantity=50, eta=TODAY)
    order_line = OrderLine(order_id="order1", product=Product("SOME-PRODUCT"), quantity=45)
    another_order_line = OrderLine(order_id="order2", product=Product("SOME-PRODUCT"), quantity=10)

    allocate(order_line, [batch])

    with pytest.raises(OutOfStock, match=another_order_line.product.title):
        allocate(another_order_line, [batch])
