from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Электронная почта', help_text="Укажите почту", unique=True)
    phone_number = models.CharField(unique=True, max_length=11, null=True, blank=True, verbose_name="Номер телефона",
                                    help_text="Укажите телефон")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='Город', help_text="Укажите город")
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name='Аватар',
                               help_text="Загрузите аватар")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
