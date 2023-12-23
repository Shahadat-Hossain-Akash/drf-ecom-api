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
    class Meta:
        model = Category
        fields = ["name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "productline")


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

    def get_attribute_value(self, obj):
        attribute_value = AttributeValue.objects.filter(
            product_line__product__id=obj.id
        )
        return AttributeValueSerializer(attribute_value, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attributes = {}
        for key in av_data:
            if key["attribute"]["id"] not in attributes:
                attributes[key["attribute"]["id"]] = [key["attribute_value"]]
            else:
                if not isinstance(attributes[key["attribute"]["id"]], list):
                    attributes[key["attribute"]["id"]] = [
                        attributes[key["attribute"]["id"]]
                    ]

                attributes[key["attribute"]["id"]].append(key["attribute_value"])

        data.update({"specifications": attributes})
        return data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "category",
            "product_line",
            "attribute",
        )

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attributes = {}
        for key in av_data:
            attributes.update({key["id"]: key["name"]})
        data.update({"type specifications": attributes})

        return data
