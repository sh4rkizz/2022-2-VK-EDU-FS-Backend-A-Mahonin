from django.shortcuts import get_object_or_404

from chats.models import Chat, ChatMember
from rest_framework.permissions import BasePermission


class IsChatAttendee(BasePermission):
    """ Permission for user to perform basic chat actions such as:
        get public chat information, send message, read message, add new chat member """

    @staticmethod
    def is_attendee(request, view):
        chat = get_object_or_404(Chat, id=view.kwargs.get('pk'))

        return chat.users.filter(id=request.user.id).exists()

    def has_permission(self, request, view):
        return self.is_attendee(request, view)


class IsChatAdmin(IsChatAttendee):
    """ Permission for user to edit chat information """

    def has_permission(self, request, view):
        member = get_object_or_404(
            ChatMember,
            chat=view.kwargs.get('pk'),
            user=request.user
        )

        return self.is_attendee(request, view) and member.is_admin


class IsChatCreator(IsChatAttendee):
    """ Permission for user to edit and delete chat """

    def has_object_permission(self, request, view, obj):
        chat = get_object_or_404(Chat, id=view.kwargs.get('pk'))

        return self.is_attendee(request, view) and chat.creator == request.user.id


class IsMessageAuthor(IsChatAttendee):
    """ Permission for user to edit, delete and NOT read message """

    def has_object_permission(self, request, view, obj):
        return self.is_attendee(request, view) and obj.author == 3


class IsUserChief(IsChatAttendee):
    """ Permission for user who invited other user to remove him from the chat """

    def has_object_permission(self, request, view, obj):
        return self.is_attendee(request, view) and obj.invited_by == request.user.id
