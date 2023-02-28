"""Views for User App."""
from django.core.mail import send_mail
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer


class SignUp(generics.CreateAPIView):
    """Class for retrive conconfirmation_code."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """GET confirmation_code."""
        if "username" not in request.data:
            response = {
                "field_not_found": "username"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if "email" not in request.data:
            response = {
                "field_not_found": "email"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        username = request.data["username"]
        email = request.data["email"]
        if User.objects.filter(username=username, email=email).exists():
            code = User.objects.filter(
                username=username, email=email
            ).get().confirmation_code
            send_mail(
                'code',
                f'confirmation_code = {code}',
                'admin@yamdb.ru',
                [email],
                fail_silently=False,
            )
            return Response(request.data, status=status.HTTP_200_OK)
        response = {
            "error": "user not found",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


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
        if User.objects.filter(
            username=username,
            confirmation_code=confirmation_code
        ).exists():
            user = User.objects.filter(
                username=username,
                confirmation_code=confirmation_code
            ).get()
            refresh = RefreshToken.for_user(user)
            response = {
                'token': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "error": "user not found",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
