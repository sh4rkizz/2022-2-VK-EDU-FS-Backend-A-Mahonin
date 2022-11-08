from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from chats.models import Chat


@require_GET
def home(request):
    return render(request, 'index.html', content_type='text/html')


@csrf_exempt
@require_GET
def chat(request):
    chat_id = request.GET.get('id')

    if chat_id:
        content = Chat.objects.get(id=chat_id)
        content = str(content)
    else:
        content = Chat.objects.all()
        content = [str(c) for c in content]

    return JsonResponse(content, safe=False)


@csrf_exempt
@require_POST
def create_chat(request):
    Chat.objects.create(companion=request.POST.get('companion'))

    return JsonResponse('200, CREATED', safe=False)


@csrf_exempt
@require_POST
def delete_chat(request):
    chat_to_delete = Chat.objects.get(id=request.POST.get('id'))
    chat_to_delete.delete()

    return JsonResponse('204 DELETED', safe=False)


@csrf_exempt
@require_POST
def edit_chat(request):
    chat_to_edit = Chat.objects.get(id=request.POST.get('id'))
    chat_to_edit.companion = request.POST.get('companion') if request.POST.get('companion') else chat_to_edit.companion
    chat_to_edit.save()

    return JsonResponse('200 EDITED', safe=False)
