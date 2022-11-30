from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView,
    RetrieveAPIView, UpdateAPIView
)
from rest_framework.response import Response

from chats.models import Chat
from chats.serializers import ChatSerializer
from users.models import User

# TODO replace mock
MOCK_USER = 2


class ChatListView(ListCreateAPIView):
    """ GET:   Retrieve chat list according available for user
        POST:  Create new chat for user and his companion """

    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(users__id=MOCK_USER).distinct()

    def create(self, request, *args, **kwargs):
        # user = get_object_or_404(User, id=self.request.user.id)
        params = self.request.data
        user = get_object_or_404(User, id=MOCK_USER)
        paired_user = get_object_or_404(User, id=params.get('pair'))

        chat = Chat(
            title=params.get('title'),
            description=params.get('description'),
            is_group_chat=bool(params.get('title')),
            creator=user
        )
        chat.save()

        chat.users.add(user, paired_user)

        return Response({'status': 'success', 'message': 'chat created'}, status=201)


class ChatInfoView(RetrieveAPIView):
    """ GET: Retrieve chat information <int:pk> """

    # permission_classes = (IsChatAttendee,)
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class ChatUpdateView(UpdateAPIView):
    """ PATCH: Update some chat fields <int:pk> """

    # permission_classes = (IsChatCreator, IsChatAdmin)
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class ChatDeleteView(DestroyAPIView):
    """ DELETE: Delete specific chat <int:pk> from messenger """

    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    # permission_classes = (IsChatCreator,)
