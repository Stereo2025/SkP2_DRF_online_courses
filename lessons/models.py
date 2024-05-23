from django.db import models

from config import settings


class Course(models.Model):
    """Модель - Курсы"""
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='course/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец', default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость')
    date_modified = models.DateTimeField(verbose_name='Дата изменения', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Модель - Уроки"""
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='lesson/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    video_url = models.URLField(max_length=200, verbose_name='Ссылка на видео', null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Курс', related_name='lessons')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец', default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-name']


class Subscriptions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='subscription')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс', related_name='subscription')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
