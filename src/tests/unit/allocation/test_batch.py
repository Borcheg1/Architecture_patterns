import pytest


def test_get_batch_by_id(batch: Batch) -> None:
    service = ...
    test_batch = service.get(batch.id)

    assert test_batch.id == batch.id


def test_allocate_order_positive(
    batch: Batch, order_line: OrderLine, product: Product
) -> None:
    batch.product = product
    order_line.product = product

    service = ...

    service.post(order_line)
    expected_quantity = batch.quantity - order_line.quantity
    batch.refresh_from_db()

    assert batch.quantity == expected_quantity


def test_allocate_order_negative(
    empty_batch: Batch, order_line: OrderLine, product: Product
) -> None:
    empty_batch.product = product
    order_line.product = product

    service = ...

    with pytest.raises("QuantityError"):
        service.post(order_line)


def test_allocate_same_line(
    batch: Batch, order_line: OrderLine, product: Product
) -> None:
    empty_batch.product = product
    order_line.product = product

    service = ...

    service.post(order_line)
    batch.refresh_from_db()

    with pytest.raises("UsedOrderLineError"):
        service.post(order_line)


def test_allocate_earlier_batch(
    batch: Batch, old_batch: Batch, order_line: OrderLine, product: Product
) -> None:
    batch.product = product
    old_batch.product = product
    order_line.product = product

    service = ...
    old_batch_quantity = old_batch.quantity
    expected_quantity = batch.quantity - order_line.quantity

    service.post(order_line)

    old_batch.refresh_from_db()
    batch.refresh_from_db()

    assert old_batch.quantity == old_batch_quantity
    assert batch.quantity == expected_quantity
