from django.db import models
from apps.bookings.models.models import Booking
from django.conf import settings

class ViewHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'view_history'
