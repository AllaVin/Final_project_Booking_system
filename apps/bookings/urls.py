# from django.urls import path
# from apps.bookings.views import views
#
# # Определяем маршруты для представлений, связанных с моделью Booking
# urlpatterns = [
#     # Эндпоинт для получения списка всех бронирований и создания нового бронирования
#     # Полный URL: http://127.0.0.1:8000/api/bookings/create/
#     path('create/', views.BookingListCreateAPIView.as_view(), name='booking-list-create'),
#
#     # Эндпоинт для получения, обновления или удаления конкретного бронирования по ID
#     # Полный URL: http://127.0.0.1:8000/api/bookings/<id>
#     # где <id> — идентификатор бронирования (например, 1)
#     path('<int:pk>/', views.BookingDetailUpdateDeleteAPIView.as_view(), name='booking-detail'),
# ]



from rest_framework.routers import DefaultRouter
from apps.bookings.views.views import BookingViewSet

router = DefaultRouter()
router.register('', BookingViewSet, basename='booking')

urlpatterns = router.urls
