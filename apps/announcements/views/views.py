from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.announcements.models.models import Announcement
from apps.announcements.serializers.serializers import AnnouncementSerializer, AnnouncementCreateUpdateSerializer
from apps.announcements.filters import AnnouncementFilter
from apps.announcements.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

# Class - на просмотр объявлений
class AnnouncementViewSet(viewsets.ModelViewSet): # viewsets.ModelViewSet - это готовый класс из DRF, который
                                                    # автоматически даёт полный набор действий:
                                                    #  list, retrieve, create, update, partial_update, destroy.

    queryset = Announcement.objects.all() # queryset - базовый набор данных
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # permission_classes - доступ только авторизованным пользователям

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] # filter_backends -
                                                    # DjangoFilterBackend — для сложной фильтрации п параметрам , например цена / кол-во комнат
                                                    # SearchFilter — для поиска по ключевым словам
                                                    # OrderingFilter — для сортировки результатов
    filterset_class = AnnouncementFilter
    search_fields = ['title', 'description']  # поиск по ключевым словам
    ordering_fields = ['price', 'created_at', 'review_count']  # сортировка по цене, дате и отзывам
    ordering = ['-review_count']  # сортировка по умолчанию: популярные (по кол-ву отзывов)

    def get_serializer_class(self): # определяем какй сериализатор будет работать в зависимости от запроса GET vs POST/PUT/PATCH
        # Для GET-запросов возвращаем сериализатор с вложенными данными
        if self.action in ['list', 'retrieve']:
            return AnnouncementSerializer
        # Для создания/обновления используем упрощённый сериализатор
        return AnnouncementCreateUpdateSerializer

    def perform_create(self, serializer):
        # при создании автоматически ставим текущего юзера владельцем
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # если landlord - видит все объявления, если tenant - видит активные
        user = self.request.user # Берём текущего пользователя, который сделал запрос. self.request — это HTTP‑запрос, .user — объект текущего авторизованного пользователя (если токен JWT есть).
        base_qs = Announcement.objects.all() # Создаём базовый QuerySet — т.е. пока берём все объявления из таблицы Announcement.

        # Если у пользователя есть атрибут role и он равен 'landlord' →
        # фильтруем объявления:
        if getattr(user, 'role', None) == 'landlord': # getattr(user, 'role', None) безопасно достаёт атрибут role (если его нет — вернёт None, не упадёт с ошибкой).
            base_qs = base_qs.filter(owner=user) # → берём только объявления этого владельца.
        # Если роль другая (или role вообще нет) →
        # фильтруем объявления:
        else:
            base_qs = base_qs.filter(status='active') # → берём только активные объявления (для арендаторов).

        # добавляем аннотацию (.annotate): количество отзывов
        return base_qs.annotate(review_count=Count('booking__review')) # Count('booking__review') — считаем количество отзывов через связанную модель:
                                                                       # booking → все бронирования, связанные с этим объявлением;
                                                                       # review → отзывы, связанные с каждым бронированием.

    # Переключение статуса (active/inactive) без полного редактирования
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def toggle_status(self, request, pk=None):
        announcement = self.get_object()
        announcement.status = 'inactive' if announcement.status == 'active' else 'active'
        announcement.save()
        return Response(AnnouncementSerializer(announcement).data, status=status.HTTP_200_OK) # возвращаем полные данные объявления через сериализатор