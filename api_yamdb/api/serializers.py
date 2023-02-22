from datetime import datetime

from rest_framework import serializers
<<<<<<< HEAD
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Genre, Title, Review
=======
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, User
>>>>>>> d93a727 (добавил валидатор UniqueTogetherValidator. Есть проблема с добавлением)



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

<<<<<<< HEAD
    def get_rating(self, obj):
        return 10


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
=======
class CurrentTitleDefault():
    '''
    Если этот класс присвоить title CurrentUserDefault() 
    title = serializers.HiddenField(default=CurrentTitleDefault()) 
    То при добавлнении ревью ошибки {"title":["This field is required."]} нет.
    А добавление не проходит так как, пользователь Anonimous
    '''
    requires_context = True

    def __call__(self, serializer_field):
        context=serializer_field.context['request'].parser_context
        '''Можно возвращать не номер из контекста, а делать get из модели
        и возваращать объект Title.'''
        return context.get('kwargs').get('title_id')

>>>>>>> d93a727 (добавил валидатор UniqueTogetherValidator. Есть проблема с добавлением)
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.SlugRelatedField(
        slug_field='id', queryset=Title.objects.all())

    class Meta:
        fields = '__all__'
        model = Review
<<<<<<< HEAD
=======

        constraints = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
>>>>>>> d93a727 (добавил валидатор UniqueTogetherValidator. Есть проблема с добавлением)
