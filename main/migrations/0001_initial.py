# Generated by Django 4.2.1 on 2023-07-16 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time', models.TimeField(verbose_name='время рассылки')),
                ('periodicity', models.CharField(choices=[('hourly', 'раз в час'), ('daily', 'раз в день'), ('weekly', 'раз в неделю'), ('monthly', 'раз в месяц')], max_length=15, verbose_name='периодичность')),
                ('mailing_status', models.CharField(choices=[('created', 'создана'), ('started', 'запущена'), ('completed', 'завершена')], default='created', max_length=15, verbose_name='статус рассылки')),
                ('is_active', models.BooleanField(default=False, verbose_name='рассылка активна')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='тема письма')),
                ('context', models.TextField(blank=True, verbose_name='тело письма')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='LogiMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_last', models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')),
                ('status', models.BooleanField(default=False, verbose_name='статус попытки')),
                ('server_answer', models.TextField(blank=True, null=True, verbose_name='ответ почтового сервера')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.message', verbose_name='сообщение')),
            ],
            options={
                'verbose_name': 'логи рассылки',
            },
        ),
    ]
