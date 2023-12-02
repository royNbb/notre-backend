from rest_framework import routers

from .views import HistoryViewSet

router = routers.SimpleRouter()
router.register(r'history', HistoryViewSet, basename='history')

urlpatterns = router.urls
