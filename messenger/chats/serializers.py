from rest_framework.serializers import ModelSerializer

from chats.models import Chat, ChatMember


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatMemberSerializer(ModelSerializer):
    class Meta:
        model = ChatMember
        fields = '__all__'
