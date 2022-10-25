from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def meta(request, user_id):
    return JsonResponse(
        {
            'user_id': user_id,
            'online': 'Was online 10 years ago'
        }
    )


@require_GET
def username(request, user_id):
    return JsonResponse(
        {
            'user_id': user_id,
            'name': 'Tigran',
            'surname': 'Mirzoyan',
            'username': 'SergeyEsenin'
        }
    )
