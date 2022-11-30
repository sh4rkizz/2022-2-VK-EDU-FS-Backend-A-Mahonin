from django.urls import path
from .views import ChatListView, ChatInfoView, ChatUpdateView, ChatDeleteView
from .views import MessageListView, MessageDeleteView, MessageUpdateView
from .views import ChatMemberListView, ChatMemberCreateView, ChatMemberDeleteView, ChatMemberUpdateView, \
    ChatMemberInfoView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('info/<int:pk>/', ChatInfoView.as_view(), name='chat'),
    path('update/<int:pk>/', ChatUpdateView.as_view(), name='chat-update'),
    path('delete/<int:pk>/', ChatDeleteView.as_view(), name='chat-delete'),

    path('poll/<int:pk>/', MessageListView.as_view(), name='message-list'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message-delete'),

    path('members/<int:chat>/', ChatMemberListView.as_view(), name='member-list'),
    path('members/<int:chat>/info/<int:user>/', ChatMemberInfoView.as_view(), name='member-list'),
    path('members/<int:chat>/add/<int:user>/', ChatMemberCreateView.as_view(), name='member-create'),
    path('members/<int:chat>/update/<int:user>/', ChatMemberUpdateView.as_view(), name='member-update'),
    path('members/<int:chat>/remove/<int:user>/', ChatMemberDeleteView.as_view(), name='member-delete'),
]
