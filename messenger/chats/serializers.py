from rest_framework.serializers import ModelSerializer, StringRelatedField
from users.serializers import UserSerializer

from .models import Chat, Message, ChatMember
from .tasks import send_email_chat_created

MESSAGE_FIELDS = ('id', 'author', 'chat', 'text', 'image', 'audio', 'timestamp', 'isRead', 'isEdited')
CHAT_FIELDS = ('id', 'title', 'description', 'isGroupChat', 'creator', 'timestamp', 'areNotificationsOn')


class LastMessageSerializer(ModelSerializer):
    chat = StringRelatedField()
    author = StringRelatedField()

    class Meta:
        model = Message
        fields = ('id', 'chat', 'author', 'text', 'image', 'audio', 'timestamp', 'isRead')
        read_only_fields = ('id', 'author', 'chat', 'timestamp')


class ChatListSerializer(ModelSerializer):
    lastMessage = LastMessageSerializer()

    class Meta:
        model = Chat
        fields = ('id', 'title', 'lastMessage')
        read_only_fields = ('id',)


class ChatSerializer(ModelSerializer):
    def create(self, validated_data):
        chat = Chat.objects.create(**validated_data)
        ChatMember.objects.create(chat=chat, user=validated_data.get('creator'), is_admin=True)

        send_email_chat_created.delay(chat_title=chat)

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
    chat = StringRelatedField()
    author = StringRelatedField()

    class Meta:
        model = Message
        fields = ('id', 'chat', 'author', 'text', 'image', 'audio', 'timestamp', 'isRead', 'isEdited')
        read_only_fields = ('id', 'author', 'chat', 'timestamp')


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
        read_only_fields = ('id', 'isRead')


class ChatMemberSerializer(ModelSerializer):
    user = UserSerializer(fields=('id', 'username', 'bio', 'isActive'))

    def create(self, validated_data):
        chat = validated_data.get('pk')

        if not ChatMember.objects.filter(chat=chat, user=validated_data.get('user')).exists():
            return chat.users.add(validated_data.get('user'))

    class Meta:
        model = ChatMember
        fields = ('chat', 'user', 'isAdmin', 'invitedBy')


class ChatMemberUpdateSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        instance.is_admin = validated_data.get('isAdmin')
        instance.save()

        return instance

    class Meta:
        model = ChatMember
        fields = ('chat', 'user', 'isAdmin')
