from django.urls import include, path
from rest_framework import routers
from users.views import NewTokenView, SignUp, UserViewSet

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    UserViewSet, ReviewViewSet, CommentViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('users', UserViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', NewTokenView.as_view()),
]
