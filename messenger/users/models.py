from django.db.models import *
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = TextField(max_length=300, blank=True, null=True, verbose_name='User biography')
    birthday = DateField(null=True, verbose_name='User birthday')

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Messenger user'
        verbose_name_plural = 'Messenger users'
