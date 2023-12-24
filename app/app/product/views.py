from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductCategorySerializer,
    ProductLine,
    ProductImage,
)
from drf_spectacular.utils import extend_schema
from django.db import connection
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import TerminalFormatter
from sqlparse import format
from django.db.models import Prefetch

# Create your views here.


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all().is_product_active()

    @extend_schema(responses=CategorySerializer, tags=["category"])
    def list(self, req):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all().is_product_active()
    lookup_field = "slug"

    @extend_schema(tags=["product"])
    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch("attribute_value__attribute"))
            .prefetch_related(Prefetch("product_line__product_image"))
            .prefetch_related(Prefetch("product_line__attribute_value__attribute")),
            many=True,
        )
        data = Response(serializer.data)

        return data

    @extend_schema(tags=["product"])
    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint to select products by category
        """
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(
                Prefetch("product_line", queryset=ProductLine.objects.order_by("order"))
            )
            .prefetch_related(
                Prefetch(
                    "product_line__product_image",
                    queryset=ProductImage.objects.order_by("order"),
                )
            ),
            many=True,
        )
        return Response(serializer.data)
