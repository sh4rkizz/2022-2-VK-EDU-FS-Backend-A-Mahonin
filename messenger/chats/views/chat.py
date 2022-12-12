from rest_framework.generics import (
    DestroyAPIView,
    RetrieveAPIView, UpdateAPIView, ListAPIView, CreateAPIView
)

from chats.models import Chat
from chats.permissions import IsChatAttendee, IsChatCreator, IsChatAdmin
from chats.serializers import ChatSerializer, ChatListSerializer, ChatInfoSerializer
from chats.tasks import send_email_chat_created


class UserChatsQuerySet:
    def get_queryset(self):
        print(self.request.user.id)
        return Chat.objects.filter(users__id=self.request.user.id)


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

# ========================================================================================================

# class ChatListView(UserChatsQuerySet, ListCreateAPIView):
#     """ GET:   Retrieve chat list according available for user
#          """
#
#     serializer_class = ChatSerializer
#
#     def get_queryset(self):
#         return Chat.objects.filter(users__id=self.request.user.id)
#
#     def create(self, request, *args, **kwargs):
#         params = self.request.data
#
#         user = get_object_or_404(User, id=self.request.user.id)
#         paired_user = get_object_or_404(User, id=params.get('pair'))
#
#         if user == paired_user:
#             return Response({'status': 'error', 'message': 'you cannot create a chat with yourself'}, status=400)
#
#         chat = Chat(
#             title=params.get('title'),
#             description=params.get('description'),
#             is_group_chat=bool(params.get('title')),
#             creator=user
#         )
#         chat.save()
#
#         chat.users.add(user, paired_user)
#
#         return Response({'status': 'success', 'message': 'chat created'}, status=201)


# class ChatInfoView(RetrieveAPIView):
#     """ GET: Retrieve chat information <int:pk> """
#
#     permission_classes = (IsChatAttendee,)
#     serializer_class = ChatInfoSerializer
#     queryset = Chat.objects.all()
#
#
# class ChatUpdateView(UpdateAPIView):
#     """ PATCH: Update some chat fields <int:pk> """
#
#     permission_classes = (IsChatCreator, IsChatAdmin)
#     serializer_class = ChatSerializer
#     queryset = Chat.objects.all()
#
#
# class ChatDeleteView(DestroyAPIView):
#     """ DELETE: Delete specific chat <int:pk> from messenger """
#
#     permission_classes = (IsChatCreator,)
#     serializer_class = ChatSerializer
#     queryset = Chat.objects.all()
