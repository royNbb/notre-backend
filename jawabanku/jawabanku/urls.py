from account.urls import router as account_router
from history.urls import router as history_router
from material.urls import router as material_router
from comment.urls import router as comment_router
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .admin import admin_site

api_v1 = DefaultRouter()
api_v1.registry.extend(account_router.registry)
api_v1.registry.extend(history_router.registry)
api_v1.registry.extend(material_router.registry)
api_v1.registry.extend(comment_router.registry)


urlpatterns = [
    path('admin/', admin_site.urls),

    path('api/v1/', include(api_v1.urls)),

    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]
