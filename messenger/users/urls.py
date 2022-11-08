from django.urls import path
from .views import user, create_user

urlpatterns = [
    path('', user, name='user info'),
    path('create', create_user, name='create new user')
]
