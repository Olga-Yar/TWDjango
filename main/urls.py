from django.urls import path

from main.apps import MainConfig
from main.views import IndexView, MessageDetailView, MessageCreateView, MessageUpdateView, MailingListView, \
    LogiListView, MessageDeleteView, ClientListView, ClientDeleteView, ClientUpdateView, ClientCreateView, MessageListView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_item'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailing/', MailingListView.as_view(), name='mailing_list'),

    path('logi/', LogiListView.as_view(), name='logi_list'),

    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]