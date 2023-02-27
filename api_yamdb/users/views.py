"""Views for User App."""
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
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
        username = request.data["username"]
        email = request.data["email"]
        try:
            user = User.objects.filter(
                username=username,
                email=email
            ).get()
            send_mail(
                'code',
                f'confirmation_code = {user.confirmation_code}',
                'admin@yamdb.ru',
                [email],
                fail_silently=False,
            )
            return Response(request.data, status=status.HTTP_200_OK)
        except:
            resp = {
                'response': str("invalid data."),
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class NewTokenView(generics.CreateAPIView):
    """Class for retrive new Auth token."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        confirmation_code = request.data["confirmation_code"]
        try:
            user = User.objects.filter(
                username=username, 
                confirmation_code=confirmation_code
            ).get()
            refresh = RefreshToken.for_user(user)
            resp = {
                'token': str(refresh.access_token),
            }
            return Response(resp, status=status.HTTP_200_OK)
        except:
            resp = {
                'response': str("invalid data."),
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
