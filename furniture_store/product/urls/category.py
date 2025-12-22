from rest_framework.routers import DefaultRouter
from product.views.category import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls
