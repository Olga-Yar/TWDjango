from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(blank=True, verbose_name='содержимое')
    image = models.ImageField(upload_to='Blog/', verbose_name='превью', **NULLABLE)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_public = models.BooleanField(default=True, verbose_name='публикация')
    num_views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} - {self.is_public}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
