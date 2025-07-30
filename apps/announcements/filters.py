import django_filters
from apps.announcements.models.models import Announcement

class AnnouncementFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    rooms_min = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    rooms_max = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    city = django_filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = Announcement
        fields = ['price_min', 'price_max', 'rooms_min', 'rooms_max', 'city', 'type']
