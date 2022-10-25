from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from time import time


@require_GET
def home(request):
    return render(request, 'index.html', content_type='text/html')


@csrf_exempt
@require_POST
def create_chat(request):
    chats = [
        {
            'chat_id': 1,
            'username': 'Martin Komitski',
            'message': 'Pushed into master? Again?...'
        }, {
            'chat_id': 2,
            'username': request.POST.get('name'),
            'message': request.POST.get('message')
        }
    ]

    return JsonResponse(chats, safe=False)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def chat(request, pk: int):
    chat_detail = {
        'chat_id': pk,
        'username': 'Erwin Schrödinger',
        'messages': [
            {
                'message_id': 1,
                'author': 'self',
                'message': 'Are u alive?',
                'time': (time() * 1000)
            },
            {
                'message_id': 2,
                'author': 'companion',
                'message': 'Relative',
                'time': (time() + 1) * 1000
            },
        ]
    }

    if request.method == 'POST':
        chat_detail['messages'].append(
            {
                'message_id': 3,
                'author': 'self',
                'message': request.POST.get('message'),
                'time': (time() + 2) * 1000
            }
        )

    return JsonResponse(chat_detail)


@require_GET
def chat_list(request):
    chat_list_with_preview = {
        'chats': [
            {
                'chat_id': 1,
                'username': 'Erwin Schrödinger',
                'message': ''
            },
            {
                'chat_id': 2,
                'username': 'Dmitrii Zaytsev',
                'message': ['Sorry, i`ve pushed into master'][-1]
            },

        ]
    }

    return JsonResponse(chat_list_with_preview)
