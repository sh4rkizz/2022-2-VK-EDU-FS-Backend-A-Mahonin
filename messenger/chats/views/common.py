from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.utils.timezone import now

from application.settings import LOGIN_URL
from users.models import User


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def logout(request):
    User.objects.filter(id=request.user.id).update(is_online=False, last_seen_at=now())

    return LogoutView.as_view(next_page=LOGIN_URL)(request)
