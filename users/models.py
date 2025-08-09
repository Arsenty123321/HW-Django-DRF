from django.contrib.auth.models import AbstractUser
from django.db import models
from lms.models import Course, Lesson


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


class Payments(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer_to_account', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Ссылка на оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Ссылка на оплаченный урок')
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма оплаты')
    method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    payment_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии')
    payment_link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Ссылка на оплату')

    def __str__(self):
        return f'Платеж {self.amount} на сумму {self.amount} от {self.user.email}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['payment_date']
