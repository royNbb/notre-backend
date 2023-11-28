from account.urls import router as account_router
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .admin import admin_site

api_v1 = DefaultRouter()
api_v1.registry.extend(account_router.registry)

urlpatterns = [
    path('admin/', admin_site.urls),

    path('api/v1/', include(api_v1.urls)),

    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]
