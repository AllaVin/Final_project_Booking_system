from django.contrib import admin
from apps.announcements.models.models import Announcement, Address

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'type', 'status', 'created_at', 'owner')
    search_fields = ('title', 'description', 'city')
    list_filter = ('type', 'status')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house_number', 'zip_code')
    search_fields = ('country', 'city', 'street')
