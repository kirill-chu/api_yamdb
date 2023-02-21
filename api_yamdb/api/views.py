from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title

from .permissions import AdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (AdminOrReadOnly,) раскоммитить после создания админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (AdminOrReadOnly,) раскоммитить после создания админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #permission_classes = (AdminOrReadOnly,) раскоммитить после создания админа
