# Generated by Django 4.2.1 on 2023-06-11 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0003_alter_order_totalcost'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regular_cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('express_cost', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
            options={
                'verbose_name': 'Delivery Cost',
                'verbose_name_plural': 'Delivery Costs',
            },
        ),
    ]
