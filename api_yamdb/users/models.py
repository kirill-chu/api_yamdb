"""Mosels for Users App."""
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ROLES = [
    ("admin", "Администратор"),
    ("moderator", "Модератор"),
    ("user", "Пользователь"),
]
regexp_validator = RegexValidator(
    r'^[\w.@+-]+\Z',
    message='not valid regexp'
)


class User(AbstractUser):

    username = models.CharField(
        'username',
        max_length=150,
        validators=[regexp_validator],
        unique=True
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=16,
        blank=True,
    )

    class Meta:
        ordering = ['username']
