from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

# from chats.views import home
from chat_messages.views import MessageViewSet
from chats.views import ChatViewSet, ChatMemberViewSet

# router.register(r'users', UserViewSet, basename='users_view_set')

api = DefaultRouter()
api.register('chats', ChatViewSet, basename='chats')
api.register('members', ChatMemberViewSet, basename='members')
api.register('messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api.urls))
]
