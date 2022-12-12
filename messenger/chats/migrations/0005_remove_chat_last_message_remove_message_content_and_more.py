# Generated by Django 4.1.2 on 2022-12-07 18:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0004_chat_creator_chat_last_message_chatmember_invited_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='last_message',
        ),
        migrations.RemoveField(
            model_name='message',
            name='content',
        ),
        migrations.AddField(
            model_name='chat',
            name='are_notifications_on',
            field=models.BooleanField(default=True, verbose_name='are_notifications_enabled_for_this_chat'),
        ),
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(max_length=10485760, null=True, upload_to='files/', verbose_name='message_image'),
        ),
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.TextField(null=True, verbose_name='message_content'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(through='chats.ChatMember', to=settings.AUTH_USER_MODEL, verbose_name='chat_users'),
        ),
    ]