# Generated by Django 4.2.1 on 2023-06-18 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0011_order_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='session_id',
        ),
    ]