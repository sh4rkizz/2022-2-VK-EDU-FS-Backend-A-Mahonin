from django.urls import path
from .views import username, meta

urlpatterns = [
    path('username/<int:user_id>', username, name='user full name info'),
    path('meta/<int:user_id>', meta, name='user meta')
]
