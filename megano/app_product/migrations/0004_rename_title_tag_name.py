# Generated by Django 4.2.1 on 2023-05-22 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0003_alter_product_category_alter_review_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='name',
        ),
    ]
