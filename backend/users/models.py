from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField('Пароль', max_length=150, blank=False)
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        'Почта',
        max_length=255,
        unique=True,
        blank=False
    )
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    is_superuser = models.BooleanField('Администратор', default=False)
    is_blocked = models.BooleanField('Блокировка', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_block(self):
        return self.is_blocked


class Follow(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        null=True
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        null=True
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow')
        ]
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'
