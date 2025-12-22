from rest_framework.generics import ListAPIView
from product.models.product import Product
from product.serializers.product import ProductSerializer

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
