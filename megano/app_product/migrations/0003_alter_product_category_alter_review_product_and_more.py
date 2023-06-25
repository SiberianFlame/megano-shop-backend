# Generated by Django 4.2.1 on 2023-05-22 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_category', '0001_initial'),
        ('app_product', '0002_alter_product_options_alter_productimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_category.category'),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_product.app_product'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='app_product.app_product'),
        ),
    ]