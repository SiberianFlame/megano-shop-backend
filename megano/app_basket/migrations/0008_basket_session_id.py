# Generated by Django 4.2.1 on 2023-06-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_basket', '0007_alter_basketproduct_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
