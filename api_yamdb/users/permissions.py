"""Permissions for Api."""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Define permissions to admin wr."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        )
