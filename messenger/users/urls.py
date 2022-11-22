from django.urls import path

from .views import *

urlpatterns = [
    path('', user_list, name='user list'),
    path('<int:pku>', user_info, name='user info'),
    path('edit/<int:pku>', edit_user, name='edit user profile')
]
