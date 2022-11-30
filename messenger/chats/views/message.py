from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView

from chats.models import Message
from chats.serializers import MessageSerializer


class MessageListView(ListCreateAPIView):
    """ GET:  Poll chat message list <int:pkc>
        POST: Create new message for chat <int:pkc> """

    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    # permission_classes = (IsChatAttendee,)


class MessageUpdateView(UpdateAPIView):
    """ PATCH: Mark specific message read <int:pkm>
            Edit specific message content <int:pkm> """

    # permission_classes = (IsMessageAuthor,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MessageDeleteView(DestroyAPIView):
    """ DELETE: Delete specific message <int:pk> """

    # permission_classes = (IsMessageAuthor,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
