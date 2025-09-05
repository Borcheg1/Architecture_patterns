from datetime import datetime, timedelta

import pytest

from src.exceptions.allocate import OutOfStock
from src.models.allocate_dto import Product, allocate
from src.tests.unit.conftest import create_order_line_by_product, prepare_batch


def test_prefers_current_stock_batches_to_shipments(product: Product) -> None:
    in_stock_batch = prepare_batch(product=product, quantity=50)
    shipment_batch = prepare_batch(
        product=product, quantity=50, eta=datetime.now() - timedelta(days=1)
    )
    order_line = create_order_line_by_product(product=product, quantity=10)

    allocate(order_line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 40
    assert shipment_batch.available_quantity == 50


def test_prefers_earlier_batches(product: Product) -> None:
    earliest = prepare_batch(product=product, quantity=50, eta=datetime.now())
    medium = prepare_batch(
        product=product, quantity=50, eta=datetime.now() + timedelta(days=1)
    )
    latest = prepare_batch(
        product=product, quantity=50, eta=datetime.now() + timedelta(days=5)
    )
    order_line = create_order_line_by_product(product=product, quantity=10)

    allocate(order_line, [medium, earliest, latest])

    assert earliest.available_quantity == 40
    assert medium.available_quantity == 50
    assert latest.available_quantity == 50


def test_returns_allocated_batch_ref(product: Product) -> None:
    in_stock_batch = prepare_batch(product=product, quantity=50)
    shipment_batch = prepare_batch(
        product=product, quantity=50, eta=datetime.now() - timedelta(days=1)
    )
    order_line = create_order_line_by_product(product=product, quantity=10)

    allocation = allocate(order_line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate(product: Product) -> None:
    batch = prepare_batch(product=product, quantity=50, eta=datetime.now())
    order_line = create_order_line_by_product(product=product, quantity=45)
    another_order_line = create_order_line_by_product(product=product, quantity=10)

    allocate(order_line, [batch])

    with pytest.raises(OutOfStock, match=another_order_line.product.title):
        allocate(another_order_line, [batch])
