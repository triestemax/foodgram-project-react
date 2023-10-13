from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Проверяем пользователя, что является атором или администратором."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or obj.author == request.user)
    

class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверяем пользователя, что является администратором."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)
