# mypy: ignore-errors
# thirdparty
import factory

# project
from src.models.domain_models import OrderLine, Product


class ProductFactory(factory.Factory):
    title = factory.Faker("sentence", nb_words=2)

    class Meta:
        model = Product


class OrderLineFactory(factory.Factory):
    order_id = factory.Faker("sentence", nb_words=1)
    product = factory.SubFactory(ProductFactory)
    quantity = 10

    class Meta:
        model = OrderLine
