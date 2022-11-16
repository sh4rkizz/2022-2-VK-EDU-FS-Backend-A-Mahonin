from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import User


@require_GET
def users(request):
    return JsonResponse({'users': [str(u) for u in get_list_or_404(User)]})


@require_GET
def info(request, pku):
    return JsonResponse(str(get_object_or_404(User, id=pku)), safe=False, status=200)


@csrf_exempt
@require_http_methods(['PATCH'])
def edit_user(request, pku):
    parameters = QueryDict(request.body)
    user = get_object_or_404(User, id=pku)

    user.username = parameters.get('uname', user.username)
    user.bio = parameters.get('bio', user.bio)
    user.first_name = parameters.get('fname', user.first_name)
    user.last_name = parameters.get('lname', user.last_name)
    user.save()

    return JsonResponse('EDITED', safe=False, status=200)
