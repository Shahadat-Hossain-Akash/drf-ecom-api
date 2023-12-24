import pytest
import json


pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = "/api/category/"

    def test_get_endpoint(self, category_factory, api_client):
        category_factory.create_batch(4, is_active=True)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoints:
    endpoint = "/api/product/"

    def test_return_single_product_by_slug(self, product_factory, api_client):
        obj = product_factory(slug="test-slug", is_active=True)
        response = api_client().get(f"{self.endpoint}{obj.slug}/")
        assert response.status_code == 200
        assert json.loads(response.content.decode("utf-8"))[0]["slug"] == "test-slug"

    def test_return_products_by_category_endpoints(
        self, category_factory, product_factory, api_client
    ):
        obj = category_factory(slug="test-slug")
        product_factory(category=obj, is_active=True)
        response = api_client().get(f"{self.endpoint}category/{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
