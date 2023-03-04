"""Views in API app."""
import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUpdateTitleSerializer, GenreSerializer,
                          MeSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer, UserSerializer)

User = get_user_model()


class GetPatchView(generics.UpdateAPIView, generics.RetrieveAPIView):
    """Get+Patch mix View."""

    pass


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Create+Destroy+list mix ViewSet."""

    pass


class CategoryViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Category instances."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Genre instances."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing Title instances."""

    queryset = Title.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """A viewset for Reviews."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsOwnerAdminModeratorOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        pass
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for Users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (permissions.IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    """A viewset for Comments."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsOwnerAdminModeratorOrReadOnly)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SignUpView(generics.CreateAPIView):
    """Class for retrive conconfirmation_code."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def get_code(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(16))

    def send_code(self, code, email):
        send_mail(
            'code',
            f'confirmation_code = {code}',
            'admin@yamdb.ru',
            [email],
            fail_silently=False,
        )

    def post(self, request):
        """GET confirmation_code."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.filter(username=username, email=email).get()
            user.confirmation_code = self.get_code()
            user.save()
            self.send_code(user.confirmation_code, user.email)
            return Response(request.data, status=status.HTTP_200_OK)
        if (User.objects.filter(email=email).exists()
           or User.objects.filter(username=username).exists()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user, _created = User.objects.get_or_create(
            username=username, email=email,
            confirmation_code=self.get_code()
        )
        user.save()
        self.send_code(user.confirmation_code, user.email)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewTokenView(generics.CreateAPIView):
    """Class for retrive new Auth token."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if "username" not in request.data:
            response = {
                "field_not_found": "username"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if "confirmation_code" not in request.data:
            response = {
                "field_not_found": "confirmation_code"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        username = request.data["username"]
        confirmation_code = request.data["confirmation_code"]
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            refresh = AccessToken.for_user(user)
            response = {
                'token': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'list', 'delete', 'patch']


class MeView(GetPatchView):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        resp = MeSerializer(request.user, context=request).data
        return Response(resp, status=status.HTTP_200_OK)

    def partial_update(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        resp = MeSerializer(request.user).data
        return Response(resp, status=status.HTTP_200_OK)
