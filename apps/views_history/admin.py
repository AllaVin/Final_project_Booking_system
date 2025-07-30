from django.contrib import admin
from apps.views_history.models.models import ViewHistory

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'booking', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('booking',)
