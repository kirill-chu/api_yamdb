"""Permissions for Api."""
from pprint import pprint
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Define permissions to admin wr."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        )


class IsModer(permissions.BasePermission):
    """Define permissions to admin wr."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'moderator'
        )


class IsUser(permissions.BasePermission):
    """Define permissions to admin wr."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'User'
        )
