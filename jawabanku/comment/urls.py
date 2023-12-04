from rest_framework import routers

from .views import CommentViewSet

router = routers.SimpleRouter()
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = router.urls
