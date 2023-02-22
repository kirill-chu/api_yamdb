from django.core.mail import send_mail
from rest_framework import filters, generics, mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User

from .permissions import AdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, UserSerializer


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class SignUp(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data["username"]
        email = request.data["email"]
        user = User.objects.filter(username=username).filter(email=email).get()
        if user:
            send_mail(
                'code',
                f'confirmation_code = {user.confirmation_code}',
                'admin@yamdb.ru',
                [email],
                fail_silently=False,
            ) 
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Token(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data["username"]
        confirmation_code = request.data["confirmation_code"]
        user = User.objects.filter(
            username=username
        ).filter(
            confirmation_code=confirmation_code
        ).get()
        if user:
            refresh = RefreshToken.for_user(user)
            response = {
                'token': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (permissions.IsAuthenticated,)
