from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView, LoginView
from .views import login, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chats/', include('chats.urls')),
    path('api/users/', include('users.urls'))


    # path('login/', login, name='login'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout')
    # path('social-auth/', include('so'))
]
