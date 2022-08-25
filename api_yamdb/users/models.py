from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.validators import MeValidate


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES_POOL = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User')
    ]
    role = models.CharField(
        'Роль',
        max_length=150,
        choices=CHOICES_POOL,
        default='user',
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=[MeValidate, UnicodeUsernameValidator()],
        max_length=150,
        unique=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ('id',)

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='Имя пользователя не может быть me'
            )
        ]
