from rest_framework import permissions


class IsChangeAuthor(permissions.BasePermission):
    """Разрешение для проверки прав доступа к предложениям."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (obj.user == request.user)
        )


class IsChangeAuthorProposal(permissions.BasePermission):
    """Разрешение для проверки прав доступа к предложениям."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (obj.ad_receiver == request.user)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для проверки прав доступа к объектам."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )
