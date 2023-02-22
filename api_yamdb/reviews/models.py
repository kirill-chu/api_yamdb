from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='author')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='title')
    text = models.TextField(verbose_name='text')
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='score')
    pub_date = models.DateTimeField(
        verbose_name='publicaton date', auto_now_add=True)
    
    class Meta:
        verbose_name ='review'
        verbose_name_plural = 'reviews'

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review' )
        ]
