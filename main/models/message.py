from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=60, verbose_name='тема письма')
    context = models.TextField(blank=True, verbose_name='тело письма')
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE(), verbose_name='рассылка', **NULLABLE)

    def __str__(self):
        return f'сообщение {self.title}: {self.mailing}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
