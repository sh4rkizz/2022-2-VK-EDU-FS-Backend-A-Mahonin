from django.urls import path

from .views import *

urlpatterns = [
    path('', users, name='user list'),
    path('<int:pku>', info, name='user info'),
    path('edit/<int:pku>', edit_user, name='edit user profile')
]
