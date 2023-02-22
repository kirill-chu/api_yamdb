from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.response import Response
from reviews.models import Category, Genre, Title, User

from .permissions import AdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, UserSerializer


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class SignUp(generics.CreateAPIView):

    def post(self, request):
        username = request.data["username"]
        email = request.data["email"]
        if User.objects.filter(username=username).filter(email=email):
            return Response(status=status.HTTP_200_OK)
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
