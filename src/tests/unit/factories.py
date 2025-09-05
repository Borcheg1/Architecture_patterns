from random import randint

import factory

from src.models.allocate_dto import OrderLine, Product


class ProductFactory(factory.Factory):
    id = randint(1, 1000000)
    title = factory.Faker("sentence", nb_words=2)

    class Meta:
        model = Product


class OrderLineFactory(factory.Factory):
    id = randint(1, 100000)
    product = factory.SubFactory(ProductFactory)
    quantity = 10

    class Meta:
        model = OrderLine
