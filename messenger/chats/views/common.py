from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import RedirectView

from application.settings import LOGOUT_REDIRECT_URL, LOGIN_URL, LOGIN_REDIRECT_URL
from users.models import User


def login(request):
    User.objects.filter(id=request.user.id).update(isOnline=True, lastSeenAt=now())

    return RedirectView.as_view(url=LOGIN_REDIRECT_URL)(request)


def home(request):
    return render(request, 'home.html')


def logout(request):
    User.objects.filter(id=request.user.id).update(isOnline=False, lastSeenAt=now())

    return LogoutView.as_view(next_page=LOGOUT_REDIRECT_URL)(request)
