from rest_framework.generics import UpdateAPIView, get_object_or_404, \
    RetrieveAPIView, ListAPIView, CreateAPIView, RetrieveDestroyAPIView

from chats.models import Message, Chat
from chats.permissions import IsChatAttendee, IsMessageAuthor, IsChatAdmin
from chats.serializers import MessageSerializer, MessagePollSerializer, MessageReadSerializer, MessageEditSerializer, \
    LastMessageSerializer
from utils import clear_tags
# from utils.publish_message import publish_message


class MessageQueryset:
    def get_queryset(self):
        return Message.objects.filter(chat=self.kwargs.get('pk'))


class MessageListView(MessageQueryset, ListAPIView):
    """ GET:  Poll chat message list <int:pk> """

    serializer_class = MessagePollSerializer
    permission_classes = (IsChatAttendee,)


class MessageCreateView(MessageQueryset, CreateAPIView):
    """ POST: Create new message for chat <int:pk> """

    serializer_class = MessageSerializer
    permission_classes = (IsChatAttendee,)

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, id=self.kwargs.get('pk'))
        self.request.data['text'] = clear_tags(self.request.data.get('text'))
        # publish_message(self.request.data)

        return serializer.save(chat=chat, author=self.request.user, text=self.request.data['text'])


class MessageRetrieveDestroy(MessageQueryset, RetrieveDestroyAPIView):
    """ GET: Retrieve specific message <int:pk>
        DELETE: Delete specific message <int:pk> """

    serializer_class = MessageSerializer

    def get_permissions(self):
        permission_classes = (
            (IsMessageAuthor, IsChatAdmin)
            if self.request.method == 'DELETE'
            else (IsChatAttendee,)
        )

        return [permission() for permission in permission_classes]


class MessageEditView(MessageQueryset, UpdateAPIView):
    """ PATCH: Edit specific message content <int:pk> """

    serializer_class = MessageEditSerializer
    permission_classes = (IsMessageAuthor, IsChatAdmin)


class MessageReadView(MessageQueryset, UpdateAPIView):
    """ PATCH: Mark specific message read <int:pk> """

    serializer_class = MessageReadSerializer
    permission_classes = (IsChatAttendee,)


class MessageLastView(RetrieveAPIView):
    """ GET: Retrieve last chat message for chat <int:pk> """

    serializer_class = LastMessageSerializer
    permission_classes = (IsChatAttendee,)

    def get_object(self):
        return Message.objects.filter(chat=self.kwargs.get('pk')).last()
