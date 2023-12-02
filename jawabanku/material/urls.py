from rest_framework import routers

from .views import AccountViewSet

router = routers.SimpleRouter()
router.register(r'users', AccountViewSet, basename='account')

urlpatterns = router.urls
