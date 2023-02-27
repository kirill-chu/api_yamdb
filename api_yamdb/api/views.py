from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django.core.mail import send_mail
from rest_framework import filters, generics, mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)

from reviews.models import Category, Genre, Title
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, CreateUpdateTitleSerializer,
                          GenreSerializer, TitleSerializer, ReviewSerializer,
                          UserSerializer)

User = get_user_model()


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Category instances."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Genre instances."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing Title instances."""

    queryset = Title.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateTitleSerializer
        return TitleSerializer
    serializer_class = TitleSerializer
    #permission_classes = (AdminOrReadOnly,) раскоммитить после создания админа


class ReviewViewSet(viewsets.ModelViewSet):
    """A viewset for Reviews."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        pass
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (permissions.IsAuthenticated,)
