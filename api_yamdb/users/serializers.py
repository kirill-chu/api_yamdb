"""Serializers file for Users App."""
from rest_framework import serializers, validators
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """User serializer for Users App."""
    email = serializers.CharField(max_length=254)
    first_name = serializers.CharField(max_length=150, required = False)
    last_name = serializers.CharField(max_length=150, required = False)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
