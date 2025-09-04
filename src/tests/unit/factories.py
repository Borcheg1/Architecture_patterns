from datetime import datetime

import factory


class ProductFactory(factory.Factory):
    title = factory.Faker("title")

    class Meta:
        model = Product


class BatchFactory(factory.Factory):
    product = factory.SubFactory(ProductFactory)
    quantity = 50
    eta = datetime.now()

    class Meta:
        model = Batch


class OrderLineFactory(factory.Factory):
    product = factory.SubFactory(ProductFactory)
    quantity = 10

    class Meta:
        model = OrderLine
