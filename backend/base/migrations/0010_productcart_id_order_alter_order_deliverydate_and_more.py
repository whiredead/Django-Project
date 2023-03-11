# Generated by Django 4.0.5 on 2022-08-21 13:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_order_deliverydate_alter_order_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcart',
            name='id_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='DeliveryDate',
            field=models.DateField(default=datetime.datetime(2022, 8, 25, 14, 2, 49, 108694)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(default='14:02:49'),
        ),
    ]
