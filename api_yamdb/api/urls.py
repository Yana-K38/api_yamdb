from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenereViewSet,
                    ReviewViewSet, TitlesViewSet, UserViewSet, confirm_code,
                    jwt_token)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenereViewSet, basename='genre')
router.register('titles', TitlesViewSet, basename='title')
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', confirm_code, name='confirm_code'),
    path('v1/auth/token/', jwt_token, name='jwt_token')
]
