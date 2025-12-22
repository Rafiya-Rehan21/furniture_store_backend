from rest_framework import viewsets
from product.models.product import Product
from product.serializers.product import ProductSerializer
from product.serializers.product_create_update import ProductCreateUpdateSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductSerializer
        return ProductCreateUpdateSerializer
