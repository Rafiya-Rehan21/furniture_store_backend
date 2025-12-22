from rest_framework import serializers
from product.models.product import Product
from product.serializers.category import CategorySerializer
from product.serializers.product_image import ProductImageSerializer
from product.serializers.product_variant import ProductVariantSerializer

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
