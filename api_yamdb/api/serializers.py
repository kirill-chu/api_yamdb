from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """A serializer for Category instances."""

    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects)]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """A serializer for Genre instances."""

    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Genre.objects)]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """A serializer for read/destroy Title instances."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')


class CreateUpdateTitleSerializer(TitleSerializer):
    """A serializer for create/update Title instances."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects, many=True
    )

    class Meta:
        fields = ('name', 'year', 'description', 'category', 'genre')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects,
                fields=('name', 'year', 'category')
            )
        ]

    def validate_year(self, value):
        if not (0 <= value <= datetime.now().year):
            raise serializers.ValidationError('Check year')
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return TitleSerializer(instance, context=context).data


class CurrentTitleDefault():
    '''Function receive title id from path parameter.'''
    requires_context = True

    def __call__(self, serializer_field):
        context=serializer_field.context['request'].parser_context
        title = get_object_or_404(
            Title, id=context.get('kwargs').get('title_id'))
        return title


class ReviewSerializer(serializers.ModelSerializer):
    '''Serializer for Review instance.'''

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.HiddenField(default =CurrentTitleDefault())

    class Meta:
        fields = '__all__'
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class CurrentReviewDefault():
    '''Function receive review id from path parameter.'''
    requires_context = True

    def __call__(self, serializer_field):
        context=serializer_field.context['request'].parser_context
        review = get_object_or_404(
            Review, id=context.get('kwargs').get('review_id'))
        return review


class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for Comment instance.'''

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    review = serializers.HiddenField(default =CurrentReviewDefault())
    
    class Meta:
        fields = '__all__'
        model = Comment
