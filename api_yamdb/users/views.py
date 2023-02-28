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
        user = get_object_or_404(User, username=username, email=email)
        send_mail(
            'code',
            f'confirmation_code = {user.confirmation_code}',
            'admin@yamdb.ru',
            [user.email],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)


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
        user = get_object_or_404(User, username=username,
                                 confirmation_code=confirmation_code)
        refresh = RefreshToken.for_user(user)
        response = {
            'token': str(refresh.access_token),
        }
        return Response(response, status=status.HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
