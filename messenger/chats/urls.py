from django.urls import path

from .views import chat, delete_chat, edit_chat, create_chat

urlpatterns = [
    path('', chat, name='chat info or chat list'),
    path('add', create_chat, name='create new chat'),
    path('delete', delete_chat, name='chat deletion'),
    path('edit', edit_chat, name='chat edition'),
]
