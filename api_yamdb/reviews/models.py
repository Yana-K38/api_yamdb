from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class BaseCategoryGenre(models.Model):
    """Общие поля для Category и Genre."""
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(BaseCategoryGenre):
    """Модель Категория."""

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'категория'


class Genre(BaseCategoryGenre):
    """Модель Жанр."""

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'жанр'


class Title(models.Model):
    """Модель Конкретного произведения"""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='название произведения',
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='год выпуска',
        validators=[validate_year]
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
    )

    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        related_name='titles',
        verbose_name='жанр',
    )

    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseAuthorTextDate(models.Model):
    """ Родительская модель с полями автор, текст и дата публикации """

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Review(BaseAuthorTextDate):
    """ Модель для отзыва """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ('title', 'pub_date')
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author',
            )
        ]

    def __str__(self) -> str:
        return self.text


class Comment(BaseAuthorTextDate):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('review', 'pub_date')

    def __str__(self) -> str:
        return self.text
