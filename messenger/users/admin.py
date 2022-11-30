from django.contrib.admin import register, ModelAdmin

from users.models import User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ['id', 'username', 'is_online', 'email', 'last_seen_at']
    ordering = ['id']
