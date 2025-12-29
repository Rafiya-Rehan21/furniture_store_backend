from rest_framework import serializers
from product.models.product import ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "product", "variant_id", "title", "price"]
