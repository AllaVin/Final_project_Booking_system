from django.db import models
from django.conf import settings
from apps.bookings.models.models import Booking

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review') # Один отзыв — к одному бронированию
                                                                                 # Один отзыв — к одному бронированию.
                                                                                # Одно бронирование — может иметь только один отзыв.
                                                                               # Следствие: нельзя оставить два отзыва на одну бронь.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
                                                                    # Один пользователь может оставить много отзывов
                                                                    # (но каждый по разным бронированиям).
                                                                    # Один отзыв принадлежит одному пользователю.
    # Итого по твоей модели:
        # Один пользователь → много отзывов (One-to-Many).
        # Одно бронирование → только один отзыв (One-to-One).
        # Один отзыв → только одно бронирование и один пользователь.

    # Практический смысл для проекта:
        # Пользователь может бронировать несколько объектов → на каждую бронь оставить ровно один отзыв.
        # Два отзыва к одному бронированию оставить нельзя.

    rating = models.PositiveSmallIntegerField()
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} for booking {self.booking.id}"
