from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.reviews.models.models import Review
from apps.reviews.serializers.serializers import ReviewSerializer
from apps.bookings.models.models import Booking
from rest_framework.exceptions import ValidationError

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']
        user = self.request.user

        # Проверка: отзыв может оставить только tenant, который бронировал
        if booking.user != self.request.user:
            raise ValidationError({"detail": "You can leave the review only for your own booking."})

        # Проверка: нельзя оставить отзыв дважды
        if Review.objects.filter(booking=booking, user=user).exists():
            raise ValidationError({"detail": "You have already left a review for this booking."})

        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='announcement/(?P<announcement_id>[^/.]+)')
    def reviews_for_announcement(self, request, announcement_id=None):
        """Все отзывы по конкретному объявлению"""
        reviews = Review.objects.filter(announcement_id=announcement_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
