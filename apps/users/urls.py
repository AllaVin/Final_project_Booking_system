from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.views import RegisterView, CustomTokenObtainPairView

urlpatterns = [
    # Эндпоинт для регистрации нового пользователя
    # Полный URL: http://127.0.0.1:8000/api/users/register/
    path('register/', RegisterView.as_view(), name='register'),

    # Эндпоинт для получения JWT токена (аутентификация)
    # Полный URL: http://127.0.0.1:8000/api/users/login/
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Эндпоинт для обновления JWT токена
    # Полный URL: http://127.0.0.1:8000/api/users/token/refresh/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]