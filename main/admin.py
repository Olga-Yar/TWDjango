from django.contrib import admin

from main.models import Mailing, Message, LogiMail


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'periodicity', 'mailing_status', 'is_active')
    search_fields = ('periodicity', 'is_active',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'context', 'mailing')
    search_fields = ('title', 'mailing',)


@admin.register(LogiMail)
class LogiMailAdmin(admin.ModelAdmin):
    list_display = ('date_last', 'status', 'server_answer', 'message')
    search_fields = ('date_last', 'status',)
