import datetime
from dataclasses import dataclass
from typing import Any

from src.exceptions.allocate import OutOfStock


@dataclass(frozen=True)
class Product:
    id: int
    title: str


@dataclass(frozen=True)
class OrderLine:
    id: int
    product: Product
    quantity: int


class Batch:
    def __init__(
        self,
        ref: str,
        product: Product,
        quantity: int,
        eta: datetime.date | None = None,
    ) -> None:
        self.reference = ref
        self.product = product
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations: set[OrderLine] = set()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: Any) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, order_line: OrderLine) -> None:
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLine) -> None:
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (
            self.product.title == order_line.product.title
            and self.available_quantity >= order_line.quantity
        )

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for title {line.product.title}")
