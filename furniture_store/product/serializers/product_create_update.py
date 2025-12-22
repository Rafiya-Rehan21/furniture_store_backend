from rest_framework import serializers
from product.models.product import Product

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
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
        ]
