from django.conf import settings
from django.contrib.auth.views import redirect_to_login

BYPASS_URLS = []
if hasattr(settings, 'LOGIN_IGNORE_URLS'):
    BYPASS_URLS += settings.LOGIN_IGNORE_URLS


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def is_bypassed(path):
        for url in BYPASS_URLS:
            if path.startswith(url):
                return True
        return False

    def process_view(self, request, func, *args, **kwargs):
        if not self.is_bypassed(request.path) and not request.user.is_authenticated:
            return redirect_to_login(next=request.path)
