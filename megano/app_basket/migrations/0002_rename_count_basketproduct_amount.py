# Generated by Django 4.2.1 on 2023-06-05 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_basket', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basketproduct',
            old_name='count',
            new_name='amount',
        ),
    ]