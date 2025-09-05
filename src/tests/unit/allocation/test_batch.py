# project
from src.models.domain_models import Product
from src.tests.unit.conftest import create_order_line_by_product, prepare_batch
from src.tests.unit.factories import ProductFactory


def test_can_allocate_if_available_greater_than_required(product: Product) -> None:
    batch = prepare_batch(product=product, quantity=50)
    order_line = create_order_line_by_product(product=product, quantity=10)
    assert batch.can_allocate(order_line) is True


def test_cannot_allocate_if_available_smaller_than_required(product: Product) -> None:
    batch = prepare_batch(product=product, quantity=10)
    order_line = create_order_line_by_product(product=product, quantity=20)
    assert batch.can_allocate(order_line) is False


def test_can_allocate_if_available_equal_to_required(product: Product) -> None:
    batch = prepare_batch(product=product, quantity=10)
    order_line = create_order_line_by_product(product=product, quantity=10)
    assert batch.can_allocate(order_line) is True


def test_cannot_allocate_if_title_do_not_match(product: Product) -> None:
    batch = prepare_batch(product=product)
    another_product = ProductFactory.build(title="SOME_PRODUCT")
    order_line = create_order_line_by_product(product=another_product)

    assert batch.can_allocate(order_line) is False


def test_can_only_deallocate_allocated_lines(product: Product) -> None:
    excepted_quantity = 10
    batch = prepare_batch(product=product, quantity=excepted_quantity)
    order_line = create_order_line_by_product(product=product, quantity=10)

    batch.deallocate(order_line)

    assert batch.available_quantity == excepted_quantity


def test_allocation_is_idempotent(product: Product) -> None:
    batch = prepare_batch(product=product, quantity=50)
    order_line = create_order_line_by_product(product=product, quantity=10)

    excepted_quantity = batch.available_quantity - order_line.quantity

    batch.allocate(order_line)
    batch.allocate(order_line)

    assert batch.available_quantity == excepted_quantity
