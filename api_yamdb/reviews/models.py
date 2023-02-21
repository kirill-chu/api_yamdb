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
    rating = models.IntegerField(blank=True, null=True) #пока нет модели
    description = models.TextField(
        blank=True, null=True, verbose_name='description'
    )
    сategory = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, #on_delete=models.SET_NULL, - нужна промежуточная модель
        related_name='titles')
    
    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name
