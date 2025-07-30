# Ограничиваем редактирование и удаление
# Landlord может редактировать/удалять только свои объявления.
# Добавим кастомное разрешение:

from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Только владелец может редактировать/удалять объявление.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем только безопасные методы для всех (GET, HEAD, OPTIONS)
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Редактировать может только владелец
        return obj.owner == request.user
