from django.db import models
from django.conf import settings


class Address(models.Model):
    country = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    house_number = models.IntegerField()
    appartment_number = models.IntegerField()
    is_elevator = models.BooleanField()

    class Meta:
        db_table = 'address'


class Announcement(models.Model):
    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    rooms = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'announcement'
