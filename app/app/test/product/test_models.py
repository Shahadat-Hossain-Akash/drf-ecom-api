from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import pytest
from app.product.models import Category, Product, ProductLine


pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        test = category_factory(name="test_str")
        assert test.__str__() == "test_str"

    def test_name_max_length(self, category_factory):
        name = "x" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = "x" * 256
        obj = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_unique_field_name(self, category_factory):
        category_factory(name="test_cat")
        with pytest.raises(IntegrityError):
            category_factory(name="test_cat")

    def test_unique_field_slug(self, category_factory):
        category_factory(slug="test_cat")
        with pytest.raises(IntegrityError):
            category_factory(slug="test_cat")

    def test_is_active_false(self, category_factory):
        obj = category_factory()
        assert obj.is_active == False

    def test_parent_category_on_delete_protect(self, category_factory):
        obj = category_factory()
        category_factory(parent=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_parent_is_null(self, category_factory):
        obj = category_factory()
        assert obj.parent is None

    def test_return_only_active_category(self, category_factory):
        ob1 = category_factory(is_active=False)
        ob2 = category_factory(is_active=True)
        qs = Category.objects.is_product_active().count()
        assert qs == 1


class TestProductModel:
    def test_str_method(self, product_factory):
        test = product_factory(name="test_product")
        assert test.__str__() == "test_product"

    def test_max_name_len(self, product_factory):
        name = "a" * 101
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_max_slug_len(self, product_factory):
        slug = "a" * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_unique_pid(self, product_factory):
        product_factory(pid="0")
        with pytest.raises(IntegrityError):
            product_factory(pid="0")

    def test_default_is_digital(self, product_factory):
        ob = product_factory()
        assert ob.is_digital == False

    def test_category_delete_protect(self, product_factory):
        ob = product_factory()
        with pytest.raises(IntegrityError):
            ob.category.delete()

    def test_fk_product_type_on_delete(self, product_factory, product_type_factory):
        ob1 = product_type_factory()
        ob2 = product_factory(product_type=ob1)
        with pytest.raises(IntegrityError):
            ob1.delete()

    def test_return_only_active_product(self, product_factory):
        ob = product_factory(is_active=True)
        ob2 = product_factory(is_active=False)
        qs = Product.objects.is_product_active().count()
        assert qs == 1

    def test_return_all_product(self, product_factory):
        ob = product_factory(is_active=True)
        ob2 = product_factory(is_active=False)
        qs = Product.objects.count()
        assert qs == 2


class TestProductLineModel:
    def test_str_method(self, product_line_factory, product_factory):
        product = product_factory.create(name="test")
        # attr = attribute_value_factory(attribute_value="test")
        test = product_line_factory.create(sku="12", product=product)
        assert test.__str__() == "test-product-line-12"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.002
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_price_max_length(self, product_line_factory):
        price = 10000000
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_sku_max_length(self, product_line_factory):
        sku = "a" * 11
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_product_on_delete(self, product_line_factory, product_factory):
        ob1 = product_factory()
        ob2 = product_line_factory(product=ob1)
        with pytest.raises(IntegrityError):
            ob1.delete()

    def test_fk_product_type_on_delete(
        self, product_line_factory, product_type_factory
    ):
        ob1 = product_type_factory()
        ob2 = product_line_factory(product_type=ob1)
        with pytest.raises(IntegrityError):
            ob1.delete()

    def test_is_active_default(self, product_line_factory):
        ob = product_line_factory()
        assert ob.is_active is False

    def test_return_active_only(self, product_line_factory):
        ob1 = product_line_factory(is_active=True)
        ob2 = product_line_factory(is_active=False)
        qs = ProductLine.objects.is_product_active().count()
        assert qs == 1

    def test_return_all_product_line(self, product_line_factory):
        ob1 = product_line_factory(is_active=True)
        ob2 = product_line_factory(is_active=False)
        qs = ProductLine.objects.count()
        assert qs == 2


class TestProductImageModel:
    def test_str_method(self, product_line_factory, product_image_factory):
        ob = product_line_factory(sku="1")
        test = product_image_factory(product_line=ob)
        assert test.__str__() == "product-line-1-image"

    def test_alternative_text_max_length(self, product_image_factory):
        x = "a" * 101
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=x)

    def test_unique_order_field(self, product_image_factory, product_line_factory):
        ob = product_line_factory()
        product_image_factory(order=1, product_line=ob)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=ob).clean()


class TestProductType:
    def test_str_method(self, product_type_factory):
        # attr = attribute_factory(name="test")
        test = product_type_factory.create(name="test_type")
        assert test.__str__() == "test_type"

    def test_name_max_length(self, product_type_factory):
        # attr = attribute_factory(name="test")
        x = "a" * 101
        ob = product_type_factory(name=x)
        with pytest.raises(ValidationError):
            ob.full_clean()


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        test = attribute_factory(name="test")
        assert test.__str__() == "test"

    def test_name_max_length(self, attribute_factory):
        # attr = attribute_factory(name="test")
        x = "a" * 101
        ob = attribute_factory(name=x)
        with pytest.raises(ValidationError):
            ob.full_clean()


class TestAttributeValueModel:
    def test_str_method(self, attribute_factory, attribute_value_factory):
        attr = attribute_factory(name="test")
        test = attribute_value_factory(attribute_value="test", attribute=attr)
        assert test.__str__() == "test-test"

    def test_attribute_value_max_length(self, attribute_value_factory):
        # attr = attribute_factory(name="test")
        x = "a" * 101
        ob = attribute_value_factory(attribute_value=x)
        with pytest.raises(ValidationError):
            ob.full_clean()


class TestProductLineAttributeValue:
    pass
