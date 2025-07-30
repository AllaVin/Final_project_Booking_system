from django.urls import path
from apps.views_history.views.views import ViewHistoryListCreateAPIView, ViewHistoryDetailUpdateDeleteAPIView

urlpatterns = [
    # Эндпоинт для получения списка истории просмотров и создания новой записи
    # Полный URL: http://127.0.0.1:8000/viewhistory/ (или /api/viewhistory/, если настроен префикс)
    path('', ViewHistoryListCreateAPIView.as_view(), name='view_history_list'),  # GET + POST

    # Эндпоинт для получения, обновления или удаления записи истории просмотров по ID
    # Полный URL: http://127.0.0.1:8000/viewhistory/<id>/ (например, /viewhistory/1/)
    path('<int:pk>/', ViewHistoryDetailUpdateDeleteAPIView.as_view(), name='view_history_detail'),  # GET + PUT/PATCH + DELETE
]