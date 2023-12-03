from rest_framework import routers

from .views import CategoryViewSet, MaterialViewSet, TagViewSet

router = routers.SimpleRouter()
router.register(r'material', MaterialViewSet, basename='material')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'tag', TagViewSet, basename='tag')

urlpatterns = router.urls
