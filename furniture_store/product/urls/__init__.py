from django.urls import path, include

urlpatterns = [
    path('', include('product.urls.category')),
    path('', include('product.urls.product')),
]
