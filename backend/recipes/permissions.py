from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверяем пользователя, что является администратором."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверяем пользователя, что является автором."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
