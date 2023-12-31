# Generated by Django 4.2.1 on 2023-05-19 06:09

from django.db import migrations, models
import app_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0003_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/def.png', null=True, upload_to=app_auth.models.profile_avatar_directory_path, verbose_name='avatar'),
        ),
    ]
