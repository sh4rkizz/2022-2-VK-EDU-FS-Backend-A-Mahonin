from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from chats.models import Chat, ChatMember
from chats.permissions import IsChatAttendee, IsUserChief
from chats.serializers import ChatMemberSerializer
from users.models import User


class ChatMemberListView(ListAPIView):
    """ GET:  Poll chat member list <int:pkc> """

    lookup_field = 'chat'
    serializer_class = ChatMemberSerializer

    def get_queryset(self):
        return get_list_or_404(ChatMember, chat=self.kwargs.get('chat'))


class ChatMemberInfoView(RetrieveAPIView):
    """ GET: Retrieve specific member <int:user> from chat <int:chat> """

    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()
    lookup_fields = ('chat', 'user')

    # permission_classes = [IsChatAttendee]

    def get_object(self):
        query_filter = {
            field: self.kwargs.get(field) for field in self.lookup_fields if
            self.kwargs.get(field) is not None
        }

        return get_object_or_404(ChatMember, **query_filter)


class ChatMemberCreateView(CreateAPIView):
    """ POST: Create new chat member <int:pku> for chat <int:pkc> """

    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()
    lookup_fields = ('chat', 'user')

    # permission_classes = (IsChatAttendee,)

    def get_object(self):
        query_filter = {
            field: self.kwargs.get(field) for field in self.lookup_fields if
            self.kwargs.get(field) is not None
        }

        return get_object_or_404(ChatMember, **query_filter)

    def perform_create(self, serializer):
        params = self.request.data

        chat = get_object_or_404(Chat, id=params.get('chat'))
        user = get_object_or_404(User, id=params.get('user'))

        if user.id in chat.users.values_list('id', flat=True):
            return Response({'status': 'error', 'message': f'User {user} is already in the chat'}, status=400)

        chat.users.add(user)

        return serializer.save(
            user=user,
            chat=chat,
            invited_by=self.request.user
        )


class ChatMemberUpdateView(UpdateAPIView):
    """ PATCH: Update member <int:user> from chat <int:chat> """

    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()
    # permission_classes = (IsUserChief, IsChatAdmin, IsChatCreator)
    lookup_fields = ('chat', 'user')

    def get_object(self):
        query_filter = {
            field: self.kwargs.get(field) for field in self.lookup_fields if
            self.kwargs.get(field) is not None
        }

        return get_object_or_404(ChatMember, **query_filter)


class ChatMemberDeleteView(DestroyAPIView):
    """ DELETE: Delete specific member <int:user> from chat <int:chat> """

    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()
    # permission_classes = (IsUserChief, IsChatAdmin, IsChatCreator)
    lookup_fields = ('chat', 'user')

    def get_object(self):
        query_filter = {
            field: self.kwargs.get(field) for field in self.lookup_fields if
            self.kwargs.get(field) is not None
        }

        return get_object_or_404(ChatMember, **query_filter)
