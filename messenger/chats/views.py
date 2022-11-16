from time import time

from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from chats.models import Chat
from chats.models import Message
from users.models import User


@require_GET
def home(request):
    return render(request, 'index.html', content_type='text/html')


@require_GET
def chat_list(request):
    return JsonResponse({'chats': [str(c) for c in get_list_or_404(Chat)]}, status=200)


@require_GET
def chat(request, pkc):
    return JsonResponse({'messages': [str(m) for m in get_list_or_404(Message, chat=pkc)]}, status=200)


@require_GET
def chat_info(request, pkc):
    return JsonResponse(str(get_object_or_404(Chat, id=pkc)), safe=False)


@require_GET
def group_chat_members(request, pkgc):
    chat_to_check = get_object_or_404(Chat, id=pkgc)

    if not chat_to_check.is_group_chat:
        return JsonResponse('This chat is a dialog', safe=False, status=403)

    return JsonResponse(
        {'members': [str(u) for u in chat_to_check.users.values_list('username', flat=True)]},
        status=200
    )


@csrf_exempt
@require_POST
def create_chat(request):
    Chat().save()

    return JsonResponse('CREATED', safe=False, status=201)


@csrf_exempt
@require_POST
def create_group_chat(request):
    title = QueryDict(request.body).get('title')

    if not title:
        return JsonResponse('You cant create a group chat with an empty title', safe=False, status=403)

    Chat(title=title, is_group_chat=True).save()

    return JsonResponse('CREATED', safe=False, status=201)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_chat(request, pkc):
    get_object_or_404(Chat, id=pkc).delete()

    return JsonResponse('DELETED', safe=False, status=204)


@csrf_exempt
@require_http_methods(['PATCH'])
def edit_chat(request, pkc):
    chat_to_edit = get_object_or_404(Chat, id=pkc)
    parameters = QueryDict(request.body)

    if not chat_to_edit.is_group_chat:
        return JsonResponse('This is not a group chat', safe=False, status=403)

    chat_to_edit.title = parameters.get('title', chat_to_edit.title)
    chat_to_edit.description = parameters.get('descr', chat_to_edit.description)
    chat_to_edit.save(update_fields=['title', 'description'])

    return JsonResponse('EDITED', safe=False, status=200)


@csrf_exempt
@require_http_methods(['PATCH'])
def add_chat_member(request, pkc, pku):
    chat_to_add = get_object_or_404(Chat, id=pkc)
    user_to_add = get_object_or_404(User, id=pku)

    if not chat_to_add.is_group_chat and chat_to_add.users.count() == 2:
        return JsonResponse('This chat is full', safe=False, status=403)

    if user_to_add.id in chat_to_add.users.values_list('id', flat=True):
        return JsonResponse(f'User {user_to_add} is already in the chat', safe=False, status=403)

    chat_to_add.users.add(user_to_add)

    return JsonResponse('EDITED', safe=False, status=200)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_chat_member(request, pkc, pku):
    chat_to_delete = get_object_or_404(Chat, id=pkc)
    user_to_delete = get_object_or_404(User, id=pku)

    if user_to_delete.id in chat_to_delete.users.values_list('id', flat=True):
        return JsonResponse(f'User {user_to_delete} is not in the chat', safe=False, status=403)

    chat_to_delete.users.remove(user_to_delete)

    return JsonResponse('DELETED', safe=False, status=204)


@csrf_exempt
@require_POST
def create_message(request, pkc):
    parameters = QueryDict(request.body)

    chat_to_send = get_object_or_404(Chat, id=pkc)
    message_author = get_object_or_404(User, id=parameters.get('author'))
    content = parameters.get('content')

    if not content:
        return JsonResponse('Unavailable message', safe=False, status=403)

    Message(
        chat=chat_to_send,
        author=message_author,
        content=content,
        status='created',
        time=int(time() * 1000)
    ).save()

    return JsonResponse('CREATED', safe=False, status=201)


@csrf_exempt
@require_http_methods(['PATCH'])
def edit_message(request, pkm):
    parameters = QueryDict(request.body)
    msg_to_edit = get_object_or_404(Message, id=pkm)

    msg_to_edit.content = parameters.get('content', msg_to_edit.content)
    msg_to_edit.is_edited = True
    msg_to_edit.save(update_fields=['content', 'is_edited'])

    return JsonResponse('EDITED', safe=False, status=200)


@csrf_exempt
@require_http_methods(['PATCH'])
def mark_read(request, pkm):
    message = get_object_or_404(Message, id=pkm)

    message.is_read = True
    message.save(update_fields=['is_read'])

    return JsonResponse('EDITED', safe=False, status=200)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_message(request, pkm):
    get_object_or_404(Message, id=pkm).delete()

    return JsonResponse('DELETED', safe=False, status=204)
