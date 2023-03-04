from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow admins to edit."""

    message = 'Adding or editting content not allowed.'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    message = "Only owner or moderator can perform this."

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user.role == 'moderator')
            or (request.user.role == 'admin')
            or (request.user.id == obj.author_id))
