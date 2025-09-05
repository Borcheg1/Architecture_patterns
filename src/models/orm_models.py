# thirdparty
from sqlalchemy.orm import registry, relationship

# fastapi
from sqlmodel import Column, DateTime, ForeignKey, Integer, String, Table

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
    Column("quantity", Integer),
    Column("eta", DateTime, nullable=True),
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
        properties={"product": relationship(product_mapper, back_populates="order_lines", lazy="joined")},
    )
    batches_mapper = mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={"product": relationship(product_mapper, back_populates="batches")},
    )
