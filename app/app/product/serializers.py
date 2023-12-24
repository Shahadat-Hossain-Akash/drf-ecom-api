from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    Attribute,
    AttributeValue,
)


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "product_line")


class ProductLineCategorySerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ["price", "product_image"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ["description"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = (
            "attribute",
            "attribute_value",
        )


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
            "attribute_value",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attributes = {}
        for key in av_data:
            if key["attribute"]["name"] not in attributes:
                attributes[key["attribute"]["name"]] = [key["attribute_value"]]
            else:
                if not isinstance(attributes[key["attribute"]["name"]], list):
                    attributes[key["attribute"]["name"]] = [
                        attributes[key["attribute"]["name"]]
                    ]

                attributes[key["attribute"]["name"]].append(key["attribute_value"])

        data.update({"properties": attributes})
        return data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "pid",
            "description",
            "category",
            "product_line",
            "attribute_value",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attributes = {}
        for key in av_data:
            attributes.update({key["attribute"]["name"]: key["attribute_value"]})
        data.update({"attributes": attributes})

        return data


class ProductCategorySerializer(serializers.ModelSerializer):
    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ("name", "slug", "pid", "created_at", "product_line")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        item = data.pop("product_line")
        if item:
            price = item[0]["price"]
            image = item[0]["product_image"]
            data.update({"price": price})
            data.update({"image": image})
        return data
