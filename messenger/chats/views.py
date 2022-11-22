from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from chat_messages.serializiers import MessageSerializer
from chats.models import Chat, ChatMember
from chat_messages.models import Message
from chats.serializers import ChatSerializer, ChatMemberSerializer
from users.models import User
from users.serializers import UserSerializer


class ChatViewSet(ViewSet):
    @staticmethod
    def list(request):
        chats = ChatSerializer(get_list_or_404(Chat), many=True).data

        return Response({'chats': chats}, status=200)

    @staticmethod
    def retrieve(request, pk=None):
        chat = ChatSerializer(get_object_or_404(Chat, id=pk)).data

        return Response(chat, status=200)

    @staticmethod
    def create(request):
        params = QueryDict(request.body)

        title = params.get('title')
        u1 = get_object_or_404(User, id=params.get('u1'))

        if title:
            chat = Chat(title=title, is_group_chat=True)
            chat.save()

            ChatMember(user=u1, chat=chat, is_admin=True, is_creator=True).save()

            return Response({'status': 'success', 'message': 'Group chat created'}, status=201)

        chat = Chat()
        chat.save()

        u2 = get_object_or_404(User, id=params.get('u2'))
        ChatMember(user=u1, chat=chat, is_admin=False, is_creator=True).save()
        ChatMember(user=u2, chat=chat, is_admin=False, is_creator=False).save()

        return Response({'status': 'success', 'message': 'Chat created'}, status=201)

    @staticmethod
    def partial_update(request, pk=None):
        chat = get_object_or_404(Chat, id=pk)
        parameters = QueryDict(request.body)

        if not chat.is_group_chat:
            return Response({'status': 'error', 'message': 'This is not a group chat'}, status=403)

        chat.title = parameters.get('title', chat.title)
        chat.description = parameters.get('description', chat.description)
        chat.save(update_fields=['title', 'description'])

        return Response({'status': 'success', 'message': 'Chat edited'}, status=200)

    @staticmethod
    def destroy(request):
        get_object_or_404(Chat, id=QueryDict(request.body).get('chat')).delete()

        return Response({'status': 'success', 'message': 'Chat deleted'}, status=204)


class ChatMemberViewSet(ViewSet):
    @staticmethod
    def retrieve(request, pk=None):
        chat_member = get_list_or_404(ChatMember, chat=pk)

        return Response({'users': ChatMemberSerializer(chat_member, many=True).data}, status=200)

    @staticmethod
    def create(request):
        chat = get_object_or_404(Chat, id=QueryDict(request.body).get('chat'))
        user = get_object_or_404(User, id=QueryDict(request.body).get('user'))

        if user.id in chat.users.values_list('id', flat=True):
            return Response({'status': 'error', 'message': f'User {user} is already in the chat'}, status=400)

        chat.users.add(user)

        return Response({'status': 'success', 'message': 'User added'}, status=200)

    @staticmethod
    def destroy(request, pk=None):
        chat = get_object_or_404(Chat, id=pk)
        user = get_object_or_404(User, id=QueryDict(request.body).get('user'))

        if chat.is_group_chat:
            return Response({'status': 'error', 'message': f'You cant remove users from dialog'}, status=403)

        if user.id in chat.users.values_list('id', flat=True):
            return Response({'status': 'error', 'message': f'User {user} is not in the chat'}, status=404)

        chat.users.remove(user)

        return Response({'status': 'success', 'message': 'User deleted'}, status=204)
