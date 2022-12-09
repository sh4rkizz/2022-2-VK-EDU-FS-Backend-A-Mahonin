from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView

from chats.models import Chat, ChatMember
from chats.permissions import IsChatAttendee, IsUserChief, IsChatAdmin, IsChatCreator
from chats.serializers import ChatMemberSerializer, ChatMemberUpdateSerializer


class GetMemberObject:
    lookup_fields = ('pk', 'user')

    def get_object(self):
        query_filter = {
            field: self.kwargs.get(field) for field in self.lookup_fields if
            self.kwargs.get(field) is not None
        }

        return get_object_or_404(ChatMember, **query_filter)


class ChatMemberCreateView(GetMemberObject, CreateAPIView):
    """ POST: Create new chat member <int:user> for chat <int:pk> """

    serializer_class = ChatMemberSerializer
    permission_classes = (IsChatAttendee,)

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, id=self.kwargs.get('chat_pk'))
        serializer.save(chat=chat)


class ChatMemberDestroyView(GetMemberObject, DestroyAPIView):
    """ DELETE: Delete specific member <int:user> from chat <int:pk> """

    serializer_class = ChatMemberSerializer
    permission_classes = (IsUserChief, IsChatAdmin)


class ChatMemberListView(GetMemberObject, ListAPIView):
    """ GET: Poll chat member list <int:pkc> """

    permission_classes = (IsChatAttendee,)
    serializer_class = ChatMemberSerializer

    def get_queryset(self):
        return get_list_or_404(ChatMember, chat=self.kwargs.get('pk'))


class ChatMemberInfoView(GetMemberObject, RetrieveAPIView):
    """ GET: Retrieve specific member <int:user> from chat <int:chat> """

    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()
    permission_classes = (IsChatAttendee,)


class ChatMemberUpdateView(GetMemberObject, UpdateAPIView):
    """ PATCH: Update member <int:user> from chat <int:pk> """

    serializer_class = ChatMemberUpdateSerializer
    permission_classes = (IsChatAdmin, IsChatCreator)
