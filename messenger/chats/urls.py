from django.urls import path
from .views import ChatListView, ChatInfoView, ChatUpdateView, ChatDeleteView, ChatCreateView
from .views import (
    MessageListView, MessageCreateView, MessageRetrieveDestroy,
    MessageEditView, MessageReadView, MessageLastView
)
from .views import (
    ChatMemberCreateView, ChatMemberDestroyView,
    ChatMemberListView, ChatMemberInfoView, ChatMemberUpdateView
)

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('new/', ChatCreateView.as_view(), name='chat-create'),
    path('info/<int:pk>/', ChatInfoView.as_view(), name='chat'),
    path('update/<int:pk>/', ChatUpdateView.as_view(), name='chat-update'),
    path('delete/<int:pk>/', ChatDeleteView.as_view(), name='chat-delete'),

    path('poll/last/<int:pk>/', MessageLastView.as_view(), name='message-last'),
    path('poll/<int:pk>/', MessageListView.as_view(), name='message-list'),
    path('poll/<int:pk>/new/', MessageCreateView.as_view(), name='message-create'),

    path('message/<int:pk>/read/', MessageReadView.as_view(), name='message-read'),
    path('message/<int:pk>/edit/', MessageEditView.as_view(), name='message-edit'),
    path('message/<int:pk>/', MessageRetrieveDestroy.as_view(), name='message-retrieve-delete'),

    path('members/<int:pk>/', ChatMemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/info/<int:user>/', ChatMemberInfoView.as_view(), name='member-list'),
    path('members/<int:pk>/add/<int:user>/', ChatMemberCreateView.as_view(), name='member-create'),
    path('members/<int:pk>/update/<int:user>/', ChatMemberUpdateView.as_view(), name='member-update'),
    path('members/<int:pk>/remove/<int:user>/', ChatMemberDestroyView.as_view(), name='member-delete'),
]
