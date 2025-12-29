from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', CartViewSet.as_view({'get': 'retrieve'}), name='cart-detail'),
    path('clear/', CartViewSet.as_view({'delete': 'clear'}), name='cart-clear'),
    path('merge/', CartViewSet.as_view({'post': 'merge'}), name='cart-merge'),
    path('', include(router.urls)),
]