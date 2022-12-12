# Generated by Django 4.1.2 on 2022-11-30 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0003_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_creator', to=settings.AUTH_USER_MODEL, verbose_name='chat_creator'),
        ),
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_message', to='chats.message', verbose_name='last_message'),
        ),
        migrations.AddField(
            model_name='chatmember',
            name='invited_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='personal_user_admin'),
        ),
        migrations.AddField(
            model_name='chatmember',
            name='is_admin',
            field=models.BooleanField(default=False, null=True, verbose_name='is_this_user_an_admin'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(default=[], through='chats.ChatMember', to=settings.AUTH_USER_MODEL, verbose_name='chat_users'),
        ),
        migrations.AlterField(
            model_name='chatmember',
            name='invitation_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='was_invited_at'),
        ),
        migrations.AlterField(
            model_name='chatmember',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='self', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(default='created', max_length=10, null=True, verbose_name='message_status'),
        ),
    ]