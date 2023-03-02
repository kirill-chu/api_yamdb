"""Views for User App."""
import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import MeSerializer, UserSerializer, SignUpSerializer


class GetPatchView(generics.UpdateAPIView, generics.RetrieveAPIView):
    pass


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
            user = User.objects.filter(
                username=username,
                email=email
            ).get()
            user.confirmation_code = self.get_code()
            user.save()
            self.send_code(user.confirmation_code, user.email)
            return Response(request.data, status=status.HTTP_200_OK)
        if (User.objects.filter(
            email=email
        ).exists() or User.objects.filter(username=username).exists()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user, created = User.objects.get_or_create(
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
            refresh = RefreshToken.for_user(user)
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
