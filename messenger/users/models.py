from django.db.models import TextField, DateField, BooleanField, DateTimeField
from django.contrib.auth.models import AbstractUser


# TODO add avatar
class User(AbstractUser):
    is_online = BooleanField(null=True, verbose_name='is_user_currently_online', default=False)
    last_seen_at = DateTimeField(null=True, verbose_name='user_last_online_time', auto_now=True)
    bio = TextField(max_length=300, blank=True, null=True, verbose_name='user_biography')
    birthday = DateField(null=True, verbose_name='user_birthday')

    # avatar = ImageField(upload_to='avatar/%Y/%m/%d', null=True, verbose_name='user_avatar')

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Messenger user'
        verbose_name_plural = 'Messenger users'
