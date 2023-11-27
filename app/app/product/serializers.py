from rest_framework import serializers
from .models import Brand, Category, Product, ProductLine, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ("id",)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "productline")


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
        )


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name")
    category = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = ("name", "slug", "description", "brand", "category", "product_line")
