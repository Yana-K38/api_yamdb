from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title

from .filter import TitlesFilter
from .mixins import MixinSetCreateListDestroy
from .permissions import (AdminOrReadOnly, AuthorAdminModeratorOrReadOnly,
                          IsAdmin)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, RegisterUserSerializer,
                          ReviewSerializer, TitlesReadSerializer,
                          TitlesWriteSerializer, TokenSerializer,
                          UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserSerializer,
    )
    def own_profile(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['role'] = request.user.role
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def confirm_code(request):
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    save_user = serializer.save()
    confirmation_code = default_token_generator.make_token(save_user)
    send_mail(
        subject='Регистрация в YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[serializer.validated_data['email']],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(
        'Неправильный код подтверждения!',
        status=status.HTTP_400_BAD_REQUEST
    )


class ReviewViewSet(viewsets.ModelViewSet):
    """ Возвращает информацию о запрашиваемых обзорах """
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date',)
    ordering = ('pub_date',)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ Возвращает информацию о запрашиваемых комментариях """
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date',)
    ordering = ('pub_date',)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(MixinSetCreateListDestroy):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategoriesSerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenereViewSet(MixinSetCreateListDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='genre_slug'
    )
    def get_genre(self, request, slug):
        genre = self.get_object()
        serializer = GenresSerializer(genre)
        genre.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlesWriteSerializer
        return TitlesReadSerializer
