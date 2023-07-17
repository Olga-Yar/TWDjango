from django.urls import path

from main.apps import MainConfig
from main.views import IndexView, MessageDetailView, MessageCreateView, MessageUpdateView, MailingListView, LogiListView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_item'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),

    path('mailing/', MailingListView.as_view(), name='mailing_list'),

    path('logi/', LogiListView.as_view(), name='logi_list'),
]