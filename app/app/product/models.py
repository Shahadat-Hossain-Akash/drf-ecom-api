from collections.abc import Collection
from django.db import models
from django.db.models.query import QuerySet
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError


class ActiveQuerySet(models.QuerySet):
    def is_product_active(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(
        max_length=235,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=False)
    objects = ActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(
        "Category",
        on_delete=models.PROTECT,
    )
    is_active = models.BooleanField(default=False)
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product"
    )
    attribute_value = models.ManyToManyField(
        "AttributeValue",
        through="ProductAttributeValue",
        related_name="product_attribute_value",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    def __str__(self):
        return f"{self.attribute.name}-{self.attribute_value}"


class ProductAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "product")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductAttributeValue, self).save(*args, **kwargs)


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_line_attribute_value_av",
    )
    product_line = models.ForeignKey(
        "ProductLine",
        on_delete=models.CASCADE,
        related_name="product_line_attribute_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "product_line")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sku = models.CharField(max_length=10)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line"
    )
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_line"
    )
    order = OrderField(unique_for_field="product", blank=True)
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    objects = ActiveQuerySet.as_manager()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name}-product-line-{self.sku}"
        # return str(self.sku)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="product_line", blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        # return str(self.url)
        return f"product-line-{self.product_line.sku}-image"


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    attribute = models.ManyToManyField(
        Attribute, through="ProductTypeAttribute", related_name="product_type"
    )

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_pt",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_a",
    )

    class Meta:
        unique_together = (
            "product_type",
            "attribute",
        )
