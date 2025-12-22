from rest_framework import viewsets
from product.models.product import ProductVariant
from product.serializers.product_variant import ProductVariantSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
