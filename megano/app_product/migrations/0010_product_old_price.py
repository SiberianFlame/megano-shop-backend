# Generated by Django 4.2.1 on 2023-06-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0009_alter_product_options_alter_productimage_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=8, null=True),
        ),
    ]
