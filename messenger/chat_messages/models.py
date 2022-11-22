from django.db.models import *

from chats.models import Chat
from users.models import User


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
