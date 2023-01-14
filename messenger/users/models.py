from django.db.models import TextField, DateField, BooleanField, DateTimeField
from django.contrib.auth.models import AbstractUser


# TODO add avatar
class User(AbstractUser):
    isOnline = BooleanField(null=True, verbose_name='is_user_currently_online', default=False)
    lastSeenAt = DateTimeField(null=True, verbose_name='user_last_online_time', auto_now=True)
    bio = TextField(max_length=300, blank=True, null=True, verbose_name='user_biography')
    birthday = DateField(null=True, verbose_name='user_birthday')

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Messenger user'
        verbose_name_plural = 'Messenger users'
