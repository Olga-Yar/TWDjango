from django.urls import path

from main.apps import MainConfig
from main.views import IndexView, MessageDetailView, MessageCreateView, MessageUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_item'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
]