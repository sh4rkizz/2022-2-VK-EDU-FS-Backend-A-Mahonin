# Generated by Django 4.1.2 on 2023-01-08 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0015_alter_message_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='are_notifications_on',
            new_name='areNotificationsOn',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='is_group_chat',
            new_name='isGroupChat',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='last_message',
            new_name='lastMessage',
        ),
        migrations.RenameField(
            model_name='chatmember',
            old_name='invitation_time',
            new_name='invitationTime',
        ),
        migrations.RenameField(
            model_name='chatmember',
            old_name='invited_by',
            new_name='invitedBy',
        ),
        migrations.RenameField(
            model_name='chatmember',
            old_name='is_admin',
            new_name='isAdmin',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='is_edited',
            new_name='isEdited',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='is_read',
            new_name='isRead',
        ),
    ]
