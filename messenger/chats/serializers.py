from rest_framework.serializers import ModelSerializer, StringRelatedField

from users.serializers import UserSerializer
from .models import Chat, Message, ChatMember
from .tasks import send_email_chat_created

MESSAGE_FIELDS = ('id', 'author', 'chat', 'text', 'image', 'audio', 'creation_time', 'is_read', 'is_edited')
CHAT_FIELDS = ('id', 'title', 'description', 'is_group_chat', 'creator', 'creation_time', 'are_notifications_on')


class ChatListSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'title', 'description')
        read_only_fields = ('id',)


class ChatSerializer(ModelSerializer):
    def create(self, validated_data):
        chat = Chat.objects.create(**validated_data)
        send_email_chat_created.delay(chat_title=validated_data.get('title'))
        ChatMember.objects.create(chat=chat, user=validated_data.get('creator'), is_admin=True)

        return chat

    class Meta:
        model = Chat
        fields = CHAT_FIELDS


class ChatInfoSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'title', 'description')


class ChatCreateSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'title', 'creator')


class MessagePollSerializer(ModelSerializer):
    author = UserSerializer(fields=('id', 'username'))
    chat = StringRelatedField()

    class Meta:
        model = Message
        fields = ('id', 'author', 'text', 'image', 'audio', 'chat', 'is_edited', 'creation_time')
        read_only_fields = ('id', 'author', 'chat', 'creation_time')


class LastMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'author', 'text', 'creation_time', 'is_read')


class MessageEditSerializer(ModelSerializer):
    chat = StringRelatedField()
    author = StringRelatedField()

    def update(self, instance, validated_data):
        instance.text = validated_data.text
        instance.is_edited = True
        instance.save()

        return instance

    class Meta:
        model = Message
        fields = MESSAGE_FIELDS
        read_only_fields = MESSAGE_FIELDS


class MessageReadSerializer(ModelSerializer):
    chat = StringRelatedField()

    def update(self, instance, validated_data):
        instance.is_read = True
        instance.save()

        return instance

    class Meta:
        model = Message
        fields = MESSAGE_FIELDS
        read_only_fields = MESSAGE_FIELDS


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = MESSAGE_FIELDS
        read_only_fields = ('id', 'is_read')


class ChatMemberSerializer(ModelSerializer):
    user = UserSerializer(fields=('id', 'username', 'bio', 'is_active'))

    def create(self, validated_data):
        chat = validated_data.get('pk')

        if not ChatMember.objects.filter(chat=chat, user=validated_data.get('user')).exists():
            return chat.users.add(validated_data.get('user'))

    class Meta:
        model = ChatMember
        fields = ('chat', 'user', 'is_admin', 'invited_by')


class ChatMemberUpdateSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        instance.is_admin = validated_data.get('is_admin')
        instance.save()

        return instance

    class Meta:
        model = ChatMember
        fields = ('chat', 'user', 'is_admin')
