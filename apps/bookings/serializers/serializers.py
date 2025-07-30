from rest_framework import serializers
from apps.announcements.models.models import Announcement
from apps.bookings.models.models import Booking
from apps.announcements.serializers.serializers import AnnouncementSerializer


class BookingCreateUpdateSerializer(serializers.ModelSerializer):
    announcement_id = serializers.PrimaryKeyRelatedField(
        queryset=Announcement.objects.all(),
        source='announcement'  # маппим на поле модели
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Booking
        fields = ['announcement_id', 'start_date', 'end_date', 'created_at', 'user']
        read_only_fields = ['created_at']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        overlapping = Booking.objects.filter(
            announcement=data['announcement'],
            status__in=['new', 'confirmed'],
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date']
        )
        if overlapping.exists():
            raise serializers.ValidationError("These dates are already booked.")
        return data



# class BookingSerializer(serializers.ModelSerializer):
#     announcement_id = AnnouncementSerializer(read_only=True)
#     user_email = serializers.EmailField(source='user.email', read_only=True)
#
#     class Meta:
#         model = Booking
#         fields = ['id', 'start_date', 'end_date', 'status', 'announcement', 'user_email', 'created_at']
#         read_only_fields = ['status', 'user_email', 'created_at']
#
# from rest_framework import serializers
# from apps.announcements.models.models import Announcement
# from apps.bookings.models.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    announcement_title = serializers.CharField(source='announcement.title', read_only=True)
    tenant_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'announcement',        # ID объявления
            'announcement_title',  # Название объявления
            'tenant_email',        # Email арендатора
            'start_date',
            'end_date',
            'status',
            'created_at',
        ]
        read_only_fields = ['status', 'user_email','created_at']

