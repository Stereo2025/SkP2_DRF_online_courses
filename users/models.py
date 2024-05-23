from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель - Пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=15, verbose_name='Телефон', null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name='Город', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    """Модель - Платежи"""

    class PaymentType(models.TextChoices):
        CASH = "CASH", "Наличные"
        TRANSFER_TO_ACCOUNT = 'TRANSFER_TO_ACCOUNT', 'Перевод на счет'

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='payment_list', default=1)
    pay_date = models.DateField(auto_now_add=True, verbose_name='Дата платежа')
    paid_course = models.ForeignKey('lessons.Course', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Оплаченный курс', related_name='payment')
    paid_lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Оплаченный урок', related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты', null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices,
                                    default='TRANSFER_TO_ACCOUNT', verbose_name="Способ оплаты")
    session_id = models.CharField(max_length=150, null=True, blank=True, verbose_name='id сессии')
    is_paid = models.BooleanField(default=False, verbose_name='статус платежа')
    payment_url = models.TextField(null=True, blank=True, verbose_name='ссылка на оплату')

    def __str__(self):
        return f'{self.user} - {self.pay_date}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
