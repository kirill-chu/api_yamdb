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
        blank=True,
    )
    role = models.TextField(
        'Роль',
        choices=ROLES,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=16,
    )
