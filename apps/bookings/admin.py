from django.contrib import admin
from apps.bookings.models.models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'user', 'start_date', 'end_date', 'status')
    search_fields = ('announcement__title', 'user__email')
    list_filter = ('status',)
