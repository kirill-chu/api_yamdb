"""Mosels for Users App."""
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ("admin", "Администратор"),
    ("moderator", "Модератор"),
    ("user", "Пользователь"),
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank = True,
    )
    role = models.CharField(
        'Роль',
        max_length = 9,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=16,
        blank = True,
    )
