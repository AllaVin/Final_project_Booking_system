"""
URL configuration for Final_project_Booking_system project.
"""
#
# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from apps.announcements.views import AnnouncementViewSet
# # from apps.bookings.views import BookingViewSet
# # from apps.reviews.views import ReviewViewSet
# # from apps.views_history.views import ViewHistoryViewSet
#
#
# router = DefaultRouter()
# router.register('announcements', AnnouncementViewSet) # http://127.0.0.1:8000/api/announcements/ - Announcement List
# router.register('bookings', BookingViewSet) # http://127.0.0.1:8000/api/bookings/ - Booking List
# router.register('reviews', ReviewViewSet) # http://127.0.0.1:8000/api/reviews/ - Review List
# router.register('views-history', ViewHistoryViewSet) # http://127.0.0.1:8000/api/views-history/ - View History List
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/users/', include('apps.users.urls')),
#     path('api/announcements/', include('apps.announcements.urls')),
#     path('api/bookings/', include('apps.bookings.urls')),
#     path('api/reviews/', include('apps.reviews.urls')),
#     path('api/views-history/', include('apps.views_history.urls')),
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users
    path('api/users/', include('apps.users.urls')), # регистрация, логин, токены

    # Announcements
    path('api/announcements/', include('apps.announcements.urls')), # CRUD для объявлений http://127.0.0.1:8000/api/announcements/

    # Bookings
    path('api/bookings/', include('apps.bookings.urls')), # CRUD для бронирований

    # Reviews
    path('api/reviews/', include('apps.reviews.urls')), # CRUD для отзывов

    # View History
    path('api/views-history/', include('apps.views_history.urls')), # CRUD для истории просмотров

]
