from django.core.mail import send_mail

from main.models import Mailing


def daily_send():
    for mail in Mailing.objects.filter(is_daily=True, status='create'):
        send_mail(mail.email, mail.title, mail.context)
