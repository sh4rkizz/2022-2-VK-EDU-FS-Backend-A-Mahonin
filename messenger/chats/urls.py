from django.urls import path

from .views import chat_list, chat, create_chat

urlpatterns = [
    path('', chat_list, name='chat list'),
    path('new', create_chat, name='create new chat'),
    path('<int:pk>', chat, name='open chat')
]
