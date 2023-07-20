from django.urls import path

from main.apps import MainConfig
from main.views import IndexView, MessageDetailView, MessageCreateView, MessageUpdateView, MailingListView, \
    LogiListView, MessageDeleteView, ClientListView, ClientDeleteView, ClientUpdateView, ClientCreateView, \
    MessageListView, ClientDetailView, BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # главная страница
    path('message/', MessageListView.as_view(), name='message_list'),  # список сообщений
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_item'),  # просмотр сообщения
    path('message/create/', MessageCreateView.as_view(), name='message_create'),  # создание сообщения
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),  # редактирование сообщения
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),  # удаление сообщения

    path('mailing/', MailingListView.as_view(), name='mailing_list'),  # список рассылок

    path('logi/', LogiListView.as_view(), name='logi_list'),  # список логов

    path('client/', ClientListView.as_view(), name='client_list'),  # список клиентов
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_item'),  # просмотр клиента
    path('client/create/', ClientCreateView.as_view(), name='client_create'),  # создание клиента
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),  # редактирование клиента
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),  # удаление клиента

    path('blog/', BlogListView.as_view(), name='blog_list'),  # список статей
    path('blog/<int:pk>', BlogDetailView.as_view(), name='blog_item'),  # просмотр статьи
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),  # создание статьи
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),  # редактирование статьи
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),  # удаление статьи
]