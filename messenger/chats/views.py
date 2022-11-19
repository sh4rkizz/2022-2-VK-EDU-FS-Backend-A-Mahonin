from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from chats.models import Chat
from chats.models import Message
from users.models import User
from utils.helpers import serialize_chat, serialize_message, serialize_user


@require_GET
def home(request):
    return render(request, 'index.html', content_type='text/html')


@require_GET
def chat_list(request):
    chats = [serialize_chat(chat) for chat in get_list_or_404(Chat)]

    return JsonResponse({'chats': chats}, status=200)


@require_GET
def chat_messages(request, pkc):
    messages = [serialize_message(message) for message in get_list_or_404(Message, chat=pkc)]

    return JsonResponse({'messages': messages}, status=200)


@require_GET
def chat_info(request, pkc):
    chat = serialize_chat(get_object_or_404(Chat, id=pkc))

    return JsonResponse(chat, status=200)


@require_GET
def group_chat_members(request, pkgc):
    chat = get_object_or_404(Chat, id=pkgc)

    if not chat.is_group_chat:
        return JsonResponse({'status': 'error', 'message': 'This chat is a dialog'}, status=403)

    members = [serialize_user(user) for user in chat.users.values_list(flat=True)]

    return JsonResponse({'members': members}, status=200)


@csrf_exempt
@require_POST
def create_chat(request):
    params = QueryDict(request.body)
    u1 = get_object_or_404(User, id=params.get('u1'))
    u2 = get_object_or_404(User, id=params.get('u2'))

    # TODO check for same users dialog creation (duplicate with different IDs)

    chat = Chat()
    chat.save()

    chat.users.add(u1)
    chat.users.add(u2)

    return JsonResponse({'status': 'success', 'message': 'Created'}, status=201)


@csrf_exempt
@require_POST
def create_group_chat(request):
    params = QueryDict(request.body)

    user = get_object_or_404(User, id=params.get('creator'))
    title = params.get('title')

    if not title:
        return JsonResponse({'status': 'error', 'message': 'Empty title for group chat'}, status=403)

    chat = Chat(title=title, is_group_chat=True)
    chat.save()

    chat.users.add(user)

    return JsonResponse({'status': 'success', 'message': 'Created'}, status=201)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_chat(request, pkc):
    get_object_or_404(Chat, id=pkc).delete()

    return JsonResponse({'status': 'success', 'message': 'Deleted'}, status=204)


@csrf_exempt
@require_http_methods(['PATCH'])
def edit_chat(request, pkc):
    chat = get_object_or_404(Chat, id=pkc)
    parameters = QueryDict(request.body)

    if not chat.is_group_chat:
        return JsonResponse({'status': 'error', 'message': 'This is not a group chat'}, status=403)

    chat.title = parameters.get('title', chat.title)
    chat.description = parameters.get('description', chat.description)
    chat.save(update_fields=['title', 'description'])

    return JsonResponse({'status': 'success', 'message': 'Edited'}, status=200)


@csrf_exempt
@require_http_methods(['PATCH'])
def add_chat_member(request, pkc, pku):
    chat = get_object_or_404(Chat, id=pkc)
    user_to_add = get_object_or_404(User, id=pku)

    if not chat.is_group_chat and chat.users.count() == 2:
        return JsonResponse({'status': 'error', 'message': 'This chat is full'}, status=403)

    if user_to_add.id in chat.users.values_list('id', flat=True):
        return JsonResponse({'status': 'error', 'message': f'User {user_to_add} is already in the chat'}, status=403)

    chat.users.add(user_to_add)

    return JsonResponse({'status': 'success', 'message': 'User added'}, status=200)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_chat_member(request, pkc, pku):
    chat = get_object_or_404(Chat, id=pkc)
    user = get_object_or_404(User, id=pku)

    if user.id in chat.users.values_list('id', flat=True):
        return JsonResponse({'status': 'error', 'message': f'User {user} is not in the chat'}, status=404)

    chat.users.remove(user)

    return JsonResponse({'status': 'success', 'message': 'Deleted'}, status=204)


@csrf_exempt
@require_POST
def create_message(request, pkc):
    parameters = QueryDict(request.body)

    chat = get_object_or_404(Chat, id=pkc)
    message_author = get_object_or_404(User, id=parameters.get('author'))
    content = parameters.get('content')

    if message_author.id not in tuple(chat.users.values_list('id', flat=True)):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized message'}, status=401)

    if not content:
        return JsonResponse({'status': 'error', 'message': 'Unavailable message'}, status=400)

    Message(
        chat=chat,
        author=message_author,
        content=content,
        status='created',
    ).save()

    return JsonResponse({'status': 'success', 'message': 'Created'}, status=201)


@csrf_exempt
@require_http_methods(['PATCH'])
def edit_message(request, pkm):
    parameters = QueryDict(request.body)
    message = get_object_or_404(Message, id=pkm)

    message.content = parameters.get('content', message.content)
    message.is_edited = True
    message.save(update_fields=['content', 'is_edited'])

    return JsonResponse({'status': 'success', 'message': 'Edited'}, status=200)


@csrf_exempt
@require_http_methods(['PATCH'])
def mark_read(request, pkm):
    message = get_object_or_404(Message, id=pkm)

    message.is_read = True
    message.save(update_fields=['is_read'])

    return JsonResponse({'status': 'success', 'message': 'Edited'}, status=200)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_message(request, pkm):
    get_object_or_404(Message, id=pkm).delete()

    return JsonResponse({'status': 'success', 'message': 'Deleted'}, status=204)
