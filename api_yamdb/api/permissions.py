from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow admins to edit."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated # позже переделать на админа
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated # позже переделать на админа
        )
