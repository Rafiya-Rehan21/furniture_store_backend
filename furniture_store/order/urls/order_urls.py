from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order.views import OrderViewSet, CheckoutViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'checkout', CheckoutViewSet, basename='checkout')

urlpatterns = [
    path('', include(router.urls)),
]