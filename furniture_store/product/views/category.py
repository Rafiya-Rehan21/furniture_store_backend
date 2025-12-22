from rest_framework.generics import ListAPIView
from product.models.category import Category
from product.serializers.category import CategorySerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
