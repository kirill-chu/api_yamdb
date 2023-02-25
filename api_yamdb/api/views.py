from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title

# from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, CreateUpdateTitleSerializer,
                          GenreSerializer, TitleSerializer)


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Category instances."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
# permission_classes = (AdminOrReadOnly,) раскоммитить после создания админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Genre instances."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
# permission_classes = (AdminOrReadOnly,) раскоммитить после создания админа
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing Title instances."""
    queryset = Title.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
# permission_classes = (AdminOrReadOnly,) раскоммитить после создания админа

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateTitleSerializer
        return TitleSerializer