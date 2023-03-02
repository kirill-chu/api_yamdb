"""Serializers file for Users App."""
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

regexp_validator = RegexValidator(
    r'^[\w.@+-]+\Z',
    message='not valid regexp'
)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[regexp_validator],
    )
    email = serializers.EmailField(
        max_length=254,
    )

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


class MeSerializer(serializers.ModelSerializer):
    """User serializer for Users App."""
    username = serializers.CharField(
        max_length=150,
        validators=[regexp_validator],
        required=False
    )
    email = serializers.EmailField(
        max_length=254,
        required=False
    )

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
        read_only_fields = ('role',)
