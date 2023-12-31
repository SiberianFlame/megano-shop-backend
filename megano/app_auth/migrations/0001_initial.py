# Generated by Django 4.2.1 on 2023-05-18 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import app_auth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='full name')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='phone')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=app_auth.models.profile_avatar_directory_path, verbose_name='avatar')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
    ]
