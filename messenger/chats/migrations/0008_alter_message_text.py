# Generated by Django 4.1.2 on 2022-12-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0007_alter_message_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='message_content'),
        ),
    ]
