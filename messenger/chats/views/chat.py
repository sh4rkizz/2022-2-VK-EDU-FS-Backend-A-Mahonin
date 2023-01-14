from chats.models import Chat
from chats.models import Message, ChatMember
from chats.permissions import IsChatAttendee, IsChatCreator, IsChatAdmin
from chats.serializers import ChatSerializer, ChatListSerializer, ChatInfoSerializer
from rest_framework.generics import (
    DestroyAPIView,
    RetrieveAPIView, UpdateAPIView, ListAPIView, CreateAPIView
)


class UserChatsQuerySet:
    def get_queryset(self):
        queryset = Chat.objects.filter(users__id=self.request.user.id)

        for chat in queryset:
            lastMessage = Message.objects.filter(chat=chat).last()

            if not chat.title:
                chat.title = ChatMember.objects.filter(chat=chat).exclude(user=self.request.user.id).last()

            chat.lastMessage = lastMessage

        return queryset


class ChatListView(UserChatsQuerySet, ListAPIView):
    """ GET: Chat list available for current user """

    serializer_class = ChatListSerializer


class ChatCreateView(CreateAPIView):
    """ POST: Create new chat """

    serializer_class = ChatSerializer


class ChatInfoView(UserChatsQuerySet, RetrieveAPIView):
    """ GET: Retrieve chat information <int:pk> """

    permission_classes = (IsChatAttendee,)
    serializer_class = ChatInfoSerializer


class ChatUpdateView(UserChatsQuerySet, UpdateAPIView):
    """ PATCH: Update some chat fields <int:pk> """

    permission_classes = (IsChatCreator, IsChatAdmin)
    serializer_class = ChatSerializer


class ChatDeleteView(UserChatsQuerySet, DestroyAPIView):
    """ DELETE: Delete specific chat <int:pk> from messenger """

    permission_classes = (IsChatCreator,)
    serializer_class = ChatSerializer
