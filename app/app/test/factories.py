import factory
from app.product.models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    Attribute,
    AttributeValue,
    ProductLineAttributeValue,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "test_category_%d" % n)
    slug = factory.Sequence(lambda n: "test_slug_%d" % n)


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "test_attribute"
    description = "test_desc"


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = "test_value"
    attribute = factory.SubFactory(AttributeFactory)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        skip_postgeneration_save = True

    name = "test_type"

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: "test_product_name_%d" % n)
    description = factory.Sequence(lambda n: "test_product_description_%d" % n)
    pid = factory.Sequence(lambda n: "0000_%d" % n)
    is_digital = False
    category = factory.SubFactory(CategoryFactory)
    is_active = False
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine
        skip_postgeneration_save = True

    price = 10.00
    sku = "12"
    stock_qty = 12
    product = factory.SubFactory(ProductFactory)
    is_active = False
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "alt text"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)


class ProductLineAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLineAttributeValue

    attribute_value = factory.SubFactory(AttributeValueFactory)
    product_line = factory.SubFactory(ProductLineFactory)
