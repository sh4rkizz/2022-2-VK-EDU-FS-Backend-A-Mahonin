# Generated by Django 4.1.2 on 2022-11-08 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='User biography'),
        ),
    ]
