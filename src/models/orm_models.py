# thirdparty
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

# project
from src.models.domain_models import Batch, OrderLine, Product

mapper_registry = registry()
metadata = mapper_registry.metadata

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(255)),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("purchased_quantity", Integer),
    Column("eta", DateTime, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("batch_id", Integer, ForeignKey("batches.id")),
    Column("order_line_id", Integer, ForeignKey("order_lines.id")),
)


def start_mappers() -> None:
    product_mapper = mapper_registry.map_imperatively(
        Product,
        products,
        properties={
            "order_lines": relationship(OrderLine, back_populates="product"),
            "batches": relationship(Batch, back_populates="product"),
        },
    )
    order_lines_mapper = mapper_registry.map_imperatively(
        OrderLine,
        order_lines,
        properties={"product": relationship(product_mapper, back_populates="order_lines")},
    )
    mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={
            "product": relationship(product_mapper, back_populates="batches"),
            "allocations": relationship(order_lines_mapper, secondary=allocations, collection_class=set),
        },
    )
