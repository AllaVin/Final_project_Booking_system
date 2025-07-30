from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.announcements.views.views import AnnouncementViewSet

# Роутер сам создаст все стандартные CRUD-эндпоинты
router = DefaultRouter()
router.register(r'', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]
