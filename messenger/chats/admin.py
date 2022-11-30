from django.contrib.admin import ModelAdmin, register
from chats.models import Chat, ChatMember, Message


@register(Chat)
class ChatAdmin(ModelAdmin):
    list_display = ['title', 'creator', 'id']


@register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ['author', 'id', 'chat']


# TODO check
@register(ChatMember)
class ChatMemberAdmin(ModelAdmin):
    list_display = ['id', 'chat', 'user']
