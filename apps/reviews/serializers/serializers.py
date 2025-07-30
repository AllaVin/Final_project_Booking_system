from rest_framework import serializers
from apps.reviews.models.models import Review
from apps.bookings.models.models import Booking

class ReviewSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        source='booking'
    )
    announcement = serializers.CharField(source='booking.announcement.title', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'booking_id', 'announcement', 'user_email', 'rating', 'text', 'created_at']
        read_only_fields = ['id', 'user_email', 'announcement', 'created_at']
