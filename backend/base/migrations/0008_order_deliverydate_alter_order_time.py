# Generated by Django 4.0.5 on 2022-08-21 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_rename_cust_order_id_cust_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='DeliveryDate',
            field=models.DateField(default=datetime.datetime(2022, 8, 25, 13, 25, 51, 828246)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(default='13:25:51'),
        ),
    ]