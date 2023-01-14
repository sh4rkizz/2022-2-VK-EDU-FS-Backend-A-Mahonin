from django.db.models import *
from users.models import User
from application.settings import AUTH_USER_MODEL


class Message(Model):
    """ Chat message model
    This models references message author and the chat this message belongs to. """

    chat = ForeignKey('Chat', verbose_name='chat', on_delete=CASCADE, null=True)
    author = ForeignKey(AUTH_USER_MODEL, verbose_name='message_author', on_delete=SET_NULL, blank=True, null=True)

    text = TextField(verbose_name='message_content', blank=True, null=True)
    image = TextField(verbose_name='message_image', null=True, blank=True)
    audio = TextField(verbose_name='message_audio', null=True, blank=True)

    isRead = BooleanField(verbose_name='message_is_read_status', default=False, null=True)
    isEdited = BooleanField(verbose_name='message_id_edited_status', default=False, null=True)

    status = CharField(max_length=10, verbose_name='message_status', default='created', null=True)
    timestamp = DateTimeField(verbose_name='message_time', auto_now_add=True)

    def __unicode__(self):
        return self.timestamp

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['timestamp']


class Chat(Model):
    """ Messenger chat model
    Chat is created by default as a dialog between two people,
    but it can be changed to be a group chat (via setting title at the creation phase). """

    creator = ForeignKey(User, verbose_name='chat_creator', null=True, on_delete=SET_NULL, related_name='chat_creator')
    lastMessage = ForeignKey(
        Message, verbose_name='chat_last_message', null=True,
        on_delete=SET_NULL, related_name='lastMessage', blank=True
    )
    users = ManyToManyField(
        AUTH_USER_MODEL, verbose_name='chat_users',
        through='ChatMember', through_fields=['chat', 'user']
    )

    areNotificationsOn = BooleanField(verbose_name='are_notifications_enabled_for_this_chat', default=True)
    title = CharField(max_length=100, verbose_name='chat_name', null=True, blank=True)
    description = CharField(max_length=256, verbose_name='chat_description', null=True, blank=True)
    isGroupChat = BooleanField(verbose_name='is_this_a_group_chat', default=False)
    timestamp = DateTimeField(verbose_name='chat_timestamp', auto_now_add=True)

    def __str__(self):
        if self.isGroupChat:
            return f'{self.title}'

        usernames = self.users.values_list('username', flat=True)

        return f'{usernames.last()}'

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class ChatMember(Model):
    chat = ForeignKey(Chat, verbose_name='chat', on_delete=CASCADE, null=True)
    user = ForeignKey(User, verbose_name='user', related_name='self', null=True, on_delete=SET_NULL)
    invitedBy = ForeignKey(User, verbose_name='personal_user_admin', null=True, on_delete=SET_NULL)
    isAdmin = BooleanField(verbose_name='is_this_user_an_admin', null=True, default=False)
    invitationTime = DateTimeField(verbose_name='was_invited_at', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Chat member'
        verbose_name_plural = 'Chat members'
