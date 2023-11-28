import factory
from app.product.models import (
    Category,
    Brand,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    Attribute,
    AttributeValue,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "Category_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: "Brand_%d" % n)


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

    name = "test_product"
    description = "test"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine
        skip_postgeneration_save = True

    price = 10.00
    sku = "12"
    stock_qty = 12
    product = factory.SubFactory(ProductFactory)
    is_active = True

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
    productline = factory.SubFactory(ProductLineFactory)
