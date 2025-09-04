import pytest


def test_get_batch_by_id(batch: Batch) -> None:
    service = ...
    test_batch = service.get(batch.id)

    assert test_batch.id == batch.id


def test_allocate_order_positive(batch: Batch, order_line: OrderLine) -> None:
    service = ...

    service.post(order_line)
    expected_quantity = batch.quantity - order_line.quantity
    batch.refresh_from_db()

    assert batch.quantity == expected_quantity


def test_allocate_order_negative(empty_batch: Batch, order_line: OrderLine) -> None:
    service = ...

    with pytest.raises("QuantityError"):
        service.post(order_line)


def test_allocate_same_line(batch: Batch, order_line: OrderLine) -> None:
    service = ...

    service.post(order_line)
    batch.refresh_from_db()

    with pytest.raises("UsedOrderLineError"):
        service.post(order_line)


def test_allocate_earlier_batch(old_batch: Batch, new_batch: Batch, order_line: OrderLine) -> None:
    service = ...
    old_batch_quantity = old_batch.quantity
    expected_quantity = new_batch.quantity - order_line.quantity

    service.post(order_line)

    old_batch.refresh_from_db()
    new_batch.refresh_from_db()

    assert old_batch.quantity == old_batch_quantity
    assert new_batch.quantity == expected_quantity
