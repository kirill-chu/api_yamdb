from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import CategoryViewSet, GenreViewSet, SignUp, TitleViewSet, Token, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', TokenObtainPairView.as_view()),
]
