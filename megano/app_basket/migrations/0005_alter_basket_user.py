# Generated by Django 4.2.1 on 2023-06-12 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_basket', '0004_alter_basketproduct_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket', to=settings.AUTH_USER_MODEL),
        ),
    ]
