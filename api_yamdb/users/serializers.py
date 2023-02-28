"""Serializers file for Users App."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Использование имени {value} '
                f'в качестве username запрещено.'
            )
        return value

    class Meta:
        fields = (
            'username',
            'email',
        )
        model = User


class UserSerializer(serializers.ModelSerializer):
    """User serializer for Users App."""

    email = serializers.CharField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

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
