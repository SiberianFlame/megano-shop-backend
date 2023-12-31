# Generated by Django 4.2.1 on 2023-06-14 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0007_sale'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'app_product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'app_product image', 'verbose_name_plural': 'app_product images'},
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_all', to='app_product.product'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='app_product.product'),
        ),
    ]
