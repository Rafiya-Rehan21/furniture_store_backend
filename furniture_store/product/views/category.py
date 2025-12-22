from rest_framework import viewsets
from product.models.category import Category
from product.serializers.category import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
