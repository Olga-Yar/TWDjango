from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    TIME_CHOICES = (
        ('hourly', 'раз в час'),
        ('daily', 'раз в день'),
        ('weekly', 'раз в неделю'),
        ('monthly', 'раз в месяц'),
    )
    STATUS_CHOICES = (
        ('created', 'создана'),
        ('started', 'запущена'),
        ('completed', 'завершена'),
    )

    mailing_time = models.TimeField(verbose_name='время рассылки')
    periodicity = models.CharField(max_length=15, choices=TIME_CHOICES, verbose_name='периодичность')
    mailing_status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='статус рассылки'
    )
    is_active = models.BooleanField(default=False, verbose_name='рассылка активна')

    def __str__(self):
        return f'{self.periodicity}, {self.mailing_status}: {self.is_active}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
