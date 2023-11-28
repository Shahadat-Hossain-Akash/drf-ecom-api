from django.core.exceptions import ValidationError
import pytest

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        test = category_factory(name="test_str")
        assert test.__str__() == "test_str"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        test = brand_factory(name="test_brand")
        assert test.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        test = product_factory(name="test_product")
        assert test.__str__() == "test_product"


class TestProductLineModel:
    def test_str_method(
        self, product_line_factory, attribute_value_factory, product_factory
    ):
        product = product_factory.create(name="test")
        attr = attribute_value_factory(attribute_value="test")
        test = product_line_factory.create(
            sku="12", attribute_value=(attr,), product=product
        )
        assert test.__str__() == "test-product-line-12"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        test = product_image_factory()
        assert test.__str__() == "test.jpg"


class TestProductType:
    def test_str_method(self, product_type_factory, attribute_factory):
        attr = attribute_factory(name="test")
        test = product_type_factory.create(name="test_type", attribute=(attr,))
        assert test.__str__() == "test_type"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        test = attribute_factory(name="test")
        assert test.__str__() == "test"


class TestAttributeValueModel:
    def test_str_method(self, attribute_factory, attribute_value_factory):
        attr = attribute_factory(name="test")
        test = attribute_value_factory(attribute_value="test", attribute=attr)
        assert test.__str__() == "test-test"
