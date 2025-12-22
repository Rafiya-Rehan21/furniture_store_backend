from django.urls import path
from product.views.category import CategoryListView
from product.views.product import ProductListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
]
