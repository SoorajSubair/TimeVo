# Generated by Django 4.1.3 on 2022-11-29 05:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0031_alter_salesreport_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesreport',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 29, 5, 58, 36, 384754, tzinfo=datetime.timezone.utc), unique=True),
        ),
    ]
