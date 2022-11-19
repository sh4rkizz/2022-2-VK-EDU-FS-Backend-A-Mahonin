from django.db.models import *

from users.models import User


class Chat(Model):
    """ Messenger chat model
    Chat is created by default as a dialog between two people,
    but it can be changed to be a group chat (via setting title at the creation phase). """

    title = CharField(max_length=100, verbose_name='chat_name', null=True)
    description = CharField(max_length=256, verbose_name='chat_description', null=True)
    is_group_chat = BooleanField(verbose_name='is_this_a_group_chat', default=False)
    creation_time = DateTimeField(verbose_name='chat_creation_time', auto_now_add=True)

    users: QuerySet = ManyToManyField(User, verbose_name='chat_users', through='ChatMember')

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
    user = ForeignKey(User, verbose_name='user', on_delete=SET_NULL, null=True)

    invitation_time = DateTimeField(verbose_name='user_invitation_in_chat_time', auto_now_add=True)

    class Meta:
        verbose_name = 'Chat member'
        verbose_name_plural = 'Chat members'


class Message(Model):
    """ Chat message model
    This models references message author and the chat this message belongs to. """

    chat = ForeignKey(Chat, verbose_name='chat', on_delete=CASCADE, null=True)
    author = ForeignKey(User, verbose_name='message_author', on_delete=SET_NULL, null=True)
    content = TextField(verbose_name='message_content')
    creation_time = DateTimeField(verbose_name='message_time', auto_now_add=True)
    status = CharField(max_length=10, verbose_name='message_status', null=True)
    is_read = BooleanField(verbose_name='message_is_read_status', default=False, null=True)
    is_edited = BooleanField(verbose_name='message_id_edited_status', default=False, null=True)

    def __str__(self):
        return f'Author: {self.author}; Message: {self.content}; Sent at {self.creation_time}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['creation_time']
