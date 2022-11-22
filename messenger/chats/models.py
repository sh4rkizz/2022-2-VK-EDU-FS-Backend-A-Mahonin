from django.db.models import *
from users.models import User


class Chat(Model):
    companion = CharField(max_length=50)

    def __str__(self):
        return f'Chat with companion: {self.companion}'

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class Message(Model):
    chat = ForeignKey(Chat, verbose_name='chat', on_delete=CASCADE, null=True)
    author = ForeignKey(User, verbose_name='message_author', on_delete=SET_NULL, null=True)
    content = CharField(max_length=256, verbose_name='message_content')
    time = DateTimeField(verbose_name='message_time', auto_now_add=True)

    def __str__(self):
        return (
            f'Author: {self.author}\n'
            f'Message: {self.content}\n'
            f'Sent at {self.time}'
        )

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['time']
