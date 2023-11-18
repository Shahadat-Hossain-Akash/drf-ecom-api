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
