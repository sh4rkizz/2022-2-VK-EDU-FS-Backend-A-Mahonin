from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import User


@require_GET
def user(request):
    user_id = request.GET.get('id')
    if user_id:
        usr = User.objects.get(id=request.GET.get('id'))
        return JsonResponse(str(usr), safe=False)

    users = User.objects.all()
    return JsonResponse([str(u) for u in users], safe=False)


@csrf_exempt
def create_user(request):
    User.objects.create(
        username=request.POST.get('username'),
        bio=request.POST.get('bio'),
        birthday=request.POST.get('bday')
    )

    return JsonResponse('200, OK')
