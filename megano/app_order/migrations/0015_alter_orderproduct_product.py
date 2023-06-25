# Generated by Django 4.2.1 on 2023-06-19 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0009_alter_product_options_alter_productimage_options'),
        ('app_order', '0014_remove_order_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='app_product.product'),
        ),
    ]
