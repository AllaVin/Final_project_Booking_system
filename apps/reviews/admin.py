from django.contrib import admin
from apps.reviews.models.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'user', 'rating', 'text', 'created_at')
    search_fields = ('user__email', 'booking__id', 'text')
    list_filter = ('rating', 'created_at')
