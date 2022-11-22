from django.http import QueryDict
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from chat_messages.models import Message
from chat_messages.serializiers import MessageSerializer
from chats.models import Chat
from users.models import User


class MessageViewSet(ViewSet):
    @staticmethod
    def list(request):
        parameters = QueryDict(request.body)
        chat = get_object_or_404(Chat, id=parameters.get('chat'))

        messages = [message for message in MessageSerializer(get_list_or_404(Message, chat=chat), many=True).data]

        return Response({'messages': messages}, status=200)

    @staticmethod
    def retrieve(request, pk=None):
        message = MessageSerializer(get_object_or_404(Message, id=pk))

        return Response(message, status=200)

    @staticmethod
    def create(request):
        parameters = QueryDict(request.body)

        chat = get_object_or_404(Chat, id=parameters.get('chat'))
        message_author = get_object_or_404(User, id=parameters.get('author'))
        content = parameters.get('content')

        if message_author.id not in tuple(chat.users.values_list('id', flat=True)):
            return Response({'status': 'error', 'message': 'Unauthorized message'}, status=401)

        if not content:
            return Response({'status': 'error', 'message': 'Unavailable message'}, status=400)

        Message(
            chat=chat,
            author=message_author,
            content=content,
            status='created'
        ).save()

        return Response({'status': 'success', 'message': 'Created'}, status=201)

    @staticmethod
    def partial_update(request, pk=None):
        parameters = QueryDict(request.body)
        message = get_object_or_404(Message, id=pk)

        message.content = parameters.get('content', message.content)
        message.is_edited = True
        message.save(update_fields=['content', 'is_edited'])

        return Response({'status': 'success', 'message': 'message edited'}, status=200)

    @staticmethod
    @action(methods=['PATCH'], detail=True)
    def mark_read(request, pk=None):
        message = get_object_or_404(Message, id=pk)

        message.is_read = True
        message.save(update_fields=['is_read'])

        return Response({'status': 'success', 'message': 'message edited'}, status=200)

    @staticmethod
    def destroy(request, pk=None):
        get_object_or_404(Message, id=pk).delete()

        return Response({'status': 'success', 'message': 'Deleted'}, status=204)
