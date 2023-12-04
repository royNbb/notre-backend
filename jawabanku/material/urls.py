from rest_framework import routers

from .views import CategoryViewSet, MaterialViewSet, TagViewSet, UploadFileViewSet

router = routers.SimpleRouter()
router.register(r'material', MaterialViewSet, basename='material')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'upload-file', UploadFileViewSet, basename='upload-file')

urlpatterns = router.urls
