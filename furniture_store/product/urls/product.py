from rest_framework.routers import DefaultRouter
from product.views.product import ProductViewSet
from product.views.product_image import ProductImageViewSet
from product.views.product_variant import ProductVariantViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='product-image')
router.register(r'product-variants', ProductVariantViewSet, basename='product-variant')

urlpatterns = router.urls
