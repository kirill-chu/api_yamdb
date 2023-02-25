"""Serializers file for Users App."""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer for Users App."""

    class Meta:
        """Meta of User serializer for Users App."""

        fields = '__all__'
        model = User
