from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from chats.views.common import home, login, logout
from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    re_path(r'^$|home/', home, name='home-page'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('social-auth/', include('drf_social_oauth2.urls', namespace='drf')),

    path('api/chats/', include('chats.urls')),
    path('api/users/', include('users.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
