from django.shortcuts import get_object_or_404

from chats.models import Chat, ChatMember
from rest_framework.permissions import BasePermission


class IsChatAttendee(BasePermission):
    @staticmethod
    def is_attendee(request, view):
        chat = get_object_or_404(Chat, view.kwargs.get('chat'))

        return request.user in chat.users.values_list('id', flat=True)

    def has_permission(self, request, view):
        return self.is_attendee(request, view)


class IsChatAdmin(IsChatAttendee):
    def has_permission(self, request, view):
        member = get_object_or_404(
            ChatMember,
            chat=view.kwargs.get('chat'),
            user=request.user
        )

        return self.is_attendee(request, view) and member.is_admin


class IsChatCreator(IsChatAttendee):
    def has_object_permission(self, request, view, obj):
        chat = get_object_or_404(Chat, view.kwargs.get('chat'))

        return self.is_attendee(request, view) and chat.creator == request.user


class IsMessageAuthor(IsChatAttendee):
    def has_object_permission(self, request, view, obj):
        return self.is_attendee(request, view) and obj.author == request.user


class IsUserChief(IsChatAttendee):
    """ Permission for user who invited other user to remove him from the chat """

    def has_object_permission(self, request, view, obj):
        member = get_object_or_404(
            ChatMember,
            chat=view.kwargs.get('chat'),
            user=request.user
        )

        return self.is_attendee(request, view) and obj.invited_by == member
