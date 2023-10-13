from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from foodgram.settings import LENGTH_NAME


class User(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Логин пользователя',
        unique=True,
        db_index=True,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Использован недопустимый символ в имени пользователя'
            ),
        )
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:LENGTH_NAME]


class Subscribe(models.Model):
    """Модель для подписчиков."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Имя подписчика'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    def __str__(self):
        return (
            f'{self.user.username[:LENGTH_NAME]} - '
            f'{self.author.username[:LENGTH_NAME]}'
        )

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]
