from rest_framework import routers

from .views import MaterialViewSet

router = routers.SimpleRouter()
router.register(r'material', MaterialViewSet, basename='material')

urlpatterns = router.urls
