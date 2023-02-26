from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='slug')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='slug')

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    year = models.IntegerField(
        validators=[
            MaxValueValidator(datetime.now().year),
            MinValueValidator(0)
        ],
        verbose_name='year'
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='description'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='category', null=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', related_name='genre'
    )

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'year', 'category'),
                name='unique_title'
            )
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title'
            )
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'
