from django.contrib.admin import register, ModelAdmin

from users.models import User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ['id', 'username', 'isOnline', 'email', 'lastSeenAt']
    ordering = ['id']
