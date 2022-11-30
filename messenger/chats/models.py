from django.db.models import *

from users.models import User
from application.settings import AUTH_USER_MODEL


class Message(Model):
    """ Chat message model
    This models references message author and the chat this message belongs to. """

    chat = ForeignKey('Chat', verbose_name='chat', on_delete=CASCADE, null=True)
    author = ForeignKey(AUTH_USER_MODEL, verbose_name='message_author', on_delete=SET_NULL, null=True)

    content = TextField(verbose_name='message_content')
    creation_time = DateTimeField(verbose_name='message_time', auto_now_add=True)
    status = CharField(max_length=10, verbose_name='message_status', default='created', null=True)
    is_read = BooleanField(verbose_name='message_is_read_status', default=False, null=True)
    is_edited = BooleanField(verbose_name='message_id_edited_status', default=False, null=True)

    def __str__(self):
        return f'Author: {self.author}; Message: {self.content}; Sent at {self.creation_time}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['creation_time']


class Chat(Model):
    """ Messenger chat model
    Chat is created by default as a dialog between two people,
    but it can be changed to be a group chat (via setting title at the creation phase). """

    creator = ForeignKey(User, verbose_name='chat_creator', null=True, on_delete=SET_NULL, related_name='chat_creator')
    last_message = ForeignKey(
        Message, verbose_name='last_message', related_name='last_message',
        null=True, blank=True, default=None, on_delete=SET_NULL
    )
    users = ManyToManyField(
        AUTH_USER_MODEL, verbose_name='chat_users', default=[],
        through='ChatMember', through_fields=['chat', 'user']
    )

    title = CharField(max_length=100, verbose_name='chat_name', null=True)
    description = CharField(max_length=256, verbose_name='chat_description', null=True)
    is_group_chat = BooleanField(verbose_name='is_this_a_group_chat', default=False)
    creation_time = DateTimeField(verbose_name='chat_creation_time', auto_now_add=True)

    def __str__(self):
        if self.is_group_chat:
            return f'Group chat {self.title}'

        if self.users.count() == 0:
            return f'Just an empty chat with id {self.id}'

        usernames = self.users.values_list('username', flat=True)

        if self.users.count() == 1:
            return f'{usernames.first()} is feeling lonely in chat {self.id}'

        return f'Chat between {usernames.first()} and {usernames.last()}'

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class ChatMember(Model):
    chat = ForeignKey(Chat, verbose_name='chat', on_delete=CASCADE, null=True)
    user = ForeignKey(User, verbose_name='user', related_name='self', null=True, on_delete=SET_NULL)
    invited_by = ForeignKey(User, verbose_name='personal_user_admin', null=True, on_delete=SET_NULL)

    is_admin = BooleanField(verbose_name='is_this_user_an_admin', null=True, default=False)

    invitation_time = DateTimeField(verbose_name='was_invited_at', auto_now_add=True)

    def __str__(self):
        return f'User {self.user.username} in chat {self.chat.title}, was invited by {self.invited_by.username}'

    class Meta:
        verbose_name = 'Chat member'
        verbose_name_plural = 'Chat members'
