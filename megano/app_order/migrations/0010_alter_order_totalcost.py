# Generated by Django 4.2.1 on 2023-06-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0009_remove_order_basket_orderproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='totalCost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
    ]
