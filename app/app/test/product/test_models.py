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
    def test_str_method(self, product_line_factory):
        test = product_line_factory(sku="12")
        assert test.__str__() == "12"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        test = product_image_factory()
        assert test.__str__() == "test.jpg"
