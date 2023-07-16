from django.db import models

NULLABLE = {'blank': True, 'null': True}


class LogiMail(models.Model):
    date_last = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    status = models.BooleanField(default=False, verbose_name='статус попытки')
    server_answer = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    message = models.ForeignKey('Message', on_delete=models.PROTECT, verbose_name='сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.date_last}: {self.status}'

    class Meta:
        verbose_name = 'логи рассылки'
