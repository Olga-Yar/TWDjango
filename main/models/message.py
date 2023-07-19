from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=60, verbose_name='тема письма')
    context = models.TextField(blank=True, verbose_name='тело письма')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, **NULLABLE,
                                verbose_name='создатель')

    def __str__(self):
        return f'сообщение {self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
