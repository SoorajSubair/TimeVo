# Generated by Django 4.1.3 on 2022-11-29 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0034_alter_salesreport_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
