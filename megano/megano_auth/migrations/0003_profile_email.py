# Generated by Django 4.2.1 on 2023-05-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('megano_auth', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='email'),
        ),
    ]
