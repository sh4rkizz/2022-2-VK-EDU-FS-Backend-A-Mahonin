from django.urls import path

from .views import *

urlpatterns = [
    # Chat URLs
    path('', chat_list, name='chat list'),
    path('<int:pkc>', chat_messages, name='chat messages'),
    path('info/<int:pkc>', chat_info, name='chat meta information'),
    path('create_chat', create_chat, name='create new chat'),
    path('delete_chat/<int:pkc>', delete_chat, name='chat deletion'),
    path('edit_chat/<int:pkc>', edit_chat, name='chat edition'),
    path('add_chat_member/<int:pkc>/<int:pku>', add_chat_member, name='add new chat member (user)'),
    path('delete_chat_member/<int:pkc>/<int:pku>', delete_chat_member, name='delete existing chat member'),

    # Group chat URLs
    path('create_group_chat', create_group_chat, name='create new group chat'),
    path('members/<int:pkgc>', group_chat_members, name='list all group chat members'),

    # Messages URLs
    path('create_message/<int:pkc>', create_message, name='create new message for chat <id>'),
    path('edit_message/<int:pkm>', edit_message, name='edit content pf the existing message'),
    path('mark_read/<int:pkm>', mark_read, name='change message status to \'read\''),
    path('delete_message/<int:pkm>', delete_message, name='delete existing message'),
]
