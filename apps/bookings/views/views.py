from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from apps.announcements.permissions import IsOwnerOrReadOnly
from apps.bookings.models.models import Booking
from apps.bookings.serializers.serializers import BookingSerializer, BookingCreateUpdateSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related('announcement', 'user')
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']  # Фильтр по статусу

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookingCreateUpdateSerializer
        return BookingSerializer

    def get_queryset(self):
        """Фильтрация по роли: тенант — свои брони, лендлорд — брони по его объявлениям."""
        user = self.request.user
        if user.role == 'tenant':
            return Booking.objects.filter(user=user).select_related('announcement', 'user')
        elif user.role == 'landlord':
            return Booking.objects.filter(announcement__owner=user).select_related('announcement', 'user')
        return Booking.objects.none()

    def perform_create(self, serializer):
        """Создание брони с проверкой роли и запретом бронировать своё объявление."""
        user = self.request.user
        announcement = serializer.validated_data.get('announcement')

        if user.role != 'tenant':
            raise ValidationError("Only tenants can create bookings.")
        if announcement.owner == user:
            raise ValidationError("You cannot book your own announcement.")
        if serializer.validated_data['start_date'] < timezone.now().date():
            raise ValidationError("Start date cannot be in the past.")

        serializer.save(user=user, status='new')

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        """Универсальный метод для смены статуса бронирования."""
        booking = self.get_object()
        action = request.data.get('action')  # 'confirm', 'reject'
        user = request.user

        if action == 'confirm':
            if booking.announcement.owner != user:
                return Response({"error": "Only the landlord can confirm bookings."}, status=403)
            if booking.status != 'new':
                return Response({"error": "Only new bookings can be confirmed."}, status=400)
            booking.status = 'confirmed'

        elif action == 'reject':
            if booking.announcement.owner != user:
                return Response({"error": "Only the landlord can reject bookings."}, status=403)
            if booking.status != 'new':
                return Response({"error": "Only new bookings can be rejected."}, status=400)
            booking.status = 'cancelled'

        else:
            return Response({"error": "Invalid action. Use 'confirm' or 'reject'."}, status=400)

        booking.save()
        return Response(BookingSerializer(booking).data)

    @action(detail=False, methods=['get'], url_path='my')
    def my_bookings(self, request):
        """Эндпоинт для получения всех бронирований текущего пользователя."""
        bookings = Booking.objects.filter(user=request.user).select_related('announcement')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='for_my_announcements')
    def for_my_announcements(self, request):
        """Все бронирования по объявлениям текущего лендлорда."""
        if request.user.role != 'landlord':
            return Response({"error": "Only landlords can view this."}, status=403)
        bookings = Booking.objects.filter(announcement__owner=request.user).select_related('announcement', 'user')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Soft delete: бронь не удаляется, а переводится в статус cancelled."""
        booking = self.get_object()
        user = request.user

        # Проверка прав
        if booking.user != user and booking.announcement.owner != user:
            return Response({"error": "You cannot cancel this booking."}, status=status.HTTP_403_FORBIDDEN)
        if timezone.now() >= booking.start_date:
            return Response({"error": "Cannot cancel booking after start date."}, status=status.HTTP_400_BAD_REQUEST)
        if booking.status == 'cancelled':
            return Response({"status": "Booking already cancelled."})

        booking.status = 'cancelled'
        booking.save()

        return Response({"status": "Booking cancelled."}, status=status.HTTP_200_OK)
