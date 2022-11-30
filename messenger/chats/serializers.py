from rest_framework.serializers import ModelSerializer

from users.serializers import UserSerializer
from utils import DynamicSerializer
from .models import Chat, Message, ChatMember


class MessageSerializer(DynamicSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat', 'author', 'content', 'creation_time', 'status', 'is_read', 'is_edited')


class ChatSerializer(ModelSerializer):
    users = UserSerializer(fields=('id', 'username'), many=True)
    last_message = MessageSerializer(fields=('id', 'author', 'content', 'creation_time', 'status', 'is_read'))

    class Meta:
        model = Chat
        fields = ('id', 'title', 'last_message', 'description', 'is_group_chat', 'creator', 'creation_time', 'users')


class ChatMemberSerializer(ModelSerializer):
    user = UserSerializer(fields=('id', 'username', 'bio', 'is_active'))

    class Meta:
        model = ChatMember
        fields = ('id', 'chat', 'user', 'invited_by', 'is_admin', 'invitation_time')
