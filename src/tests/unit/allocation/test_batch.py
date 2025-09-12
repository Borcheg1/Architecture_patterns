# project
from src.models.domain_models import Batch, OrderLine, Product


def test_can_allocate_if_available_greater_than_required(batch: Batch, order_line: OrderLine) -> None:
    batch.purchased_quantity = 50
    order_line.quantity = 10

    assert batch.can_allocate(order_line) is True


def test_cannot_allocate_if_available_smaller_than_required(batch: Batch, order_line: OrderLine) -> None:
    batch.purchased_quantity = 10
    order_line.quantity = 20

    assert batch.can_allocate(order_line) is False


def test_can_allocate_if_available_equal_to_required(batch: Batch, order_line: OrderLine) -> None:
    batch.purchased_quantity = 10
    order_line.quantity = 10

    assert batch.can_allocate(order_line) is True


def test_cannot_allocate_if_title_do_not_match(batch: Batch, order_line: OrderLine) -> None:
    another_product = Product(title="SOME_PRODUCT")
    order_line.product = another_product

    assert batch.can_allocate(order_line) is False


def test_can_only_deallocate_allocated_lines(batch: Batch, order_line: OrderLine) -> None:
    excepted_quantity = batch.purchased_quantity
    batch.deallocate(order_line)

    assert batch.available_quantity == excepted_quantity


def test_allocation_is_idempotent(batch: Batch, order_line: OrderLine) -> None:
    batch.purchased_quantity = 20
    order_line.quantity = 2
    excepted_quantity = batch.purchased_quantity - order_line.quantity

    batch.allocate(order_line)
    batch.allocate(order_line)

    assert batch.available_quantity == excepted_quantity
