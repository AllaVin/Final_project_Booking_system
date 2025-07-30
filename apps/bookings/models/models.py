from django.db import models
from django.conf import settings
from apps.announcements.models.models import Announcement

class Booking(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)  # теперь авто

    class Meta:
        db_table = 'booking'

    def __str__(self):
        return f"{self.user.email} - {self.announcement.title}"
