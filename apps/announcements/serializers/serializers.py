from rest_framework import serializers
from apps.announcements.models.models import Announcement, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'country',
            'zip_code',
            'city',
            'street',
            'house_number',
            'appartment_number',
            'is_elevator']


class AnnouncementSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)  # при GET вернём вложенный объект адреса
    owner_email = serializers.EmailField(source='owner.email', read_only=True)  # для удобства — email владельца
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id',
            'title',
            'description',
            'price',
            'address',
            'rooms',
            'type',
            'status',
            'created_at',
            'owner_email',
            'review_count'
        ]


class AnnouncementCreateUpdateSerializer(serializers.ModelSerializer):
    # Принимаем ID и сохраняем его в поле address модели
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        source='address'
    )
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # автоматически ставим текущего юзера
    created_at = serializers.DateTimeField(read_only=True)  # автоматическое заполнение

    class Meta:
        model = Announcement
        fields = [
            'title',
            'description',
            'price',
            'address_id',  # только id
            'rooms',
            'type',
            'status',
            'created_at',
            'owner',
        ]