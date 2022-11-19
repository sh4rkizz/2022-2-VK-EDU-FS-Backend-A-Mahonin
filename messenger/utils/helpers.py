from chats.views import Chat, Message
from users.models import User


def serialize_chat(chat: Chat):
    return {
        'id': chat.id,
        'creation_time': chat.creation_time,
        'title': chat.title,
        'description': chat.description,
        'is_group_chat': chat.is_group_chat,
        'users': list(chat.users.values('id', 'username'))
    }


def serialize_message(message: Message):
    return {
        'id': message.id,
        'author': serialize_user(message.author),
        'content': message.content,
        'creation_time': message.creation_time,
        'status': message.status,
        'is_read': message.is_read,
        'is_edited': message.is_edited
    }


def serialize_user(user: User):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'second_name': user.last_name,
        'bio': user.bio,
        'birthday': user.birthday
    }
