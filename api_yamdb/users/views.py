"""Views for User App."""
from django.core.mail import send_mail
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, SugnUpSerializer, TokenSerializer


class SignUp(generics.CreateAPIView):
    """Class for retrive conconfirmation_code."""
    serializer_class = SugnUpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """GET confirmation_code."""
        serializer = self.get_serializer(data=request.data)
        print("111111")
        if serializer.is_valid():
            print("22222")
            if User.objects.filter(
                username=serializer["username"],
                email=serializer["email"]
            ).exists():
                send_mail(
                    'code',
                    f'confirmation_code = {serializer["username"]}',
                    'admin@yamdb.ru',
                    [serializer["email"]],
                    fail_silently=False,
                )
                return Response(request.data, status=status.HTTP_200_OK)
            response = {
                'response': str('not such user')
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewTokenView(generics.CreateAPIView):
    """Class for retrive new Auth token."""
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(
                username=serializer["username"],
                confirmation_code=serializer["confirmation_code"]
            ).exists():
                refresh = RefreshToken.for_user(user)
                resp = {
                    'token': str(refresh.access_token),
                }
                return Response(resp, status=status.HTTP_200_OK)
            response = {
                'response': str('not such user')
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
