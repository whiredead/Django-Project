# Generated by Django 4.0.5 on 2022-08-21 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_order_deliverydate_alter_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='DeliveryDate',
            field=models.DateField(default=datetime.datetime(2022, 8, 25, 14, 1, 6, 809938)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(default='14:01:06'),
        ),
    ]