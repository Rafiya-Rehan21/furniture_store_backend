from rest_framework import serializers
from product.models.product import Product, ProductImage, ProductVariant
from product.serializers.category import CategorySerializer

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image_url"]

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "variant_id", "title", "price"]

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "general_category",
            "vendor",
            "categories",
            "free_shipping",
            "available",
            "sold",
            "items_in_stock",
            "created_at",
            "images",
            "variants",
        ]
