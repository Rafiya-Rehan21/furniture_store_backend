from rest_framework import viewsets
from product.models.product import ProductImage
from product.serializers.product_image import ProductImageSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
