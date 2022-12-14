# Generated by Django 4.1.3 on 2022-12-07 08:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0053_alter_categoryoffer_offer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_home.order')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_home.orderitem')),
            ],
        ),
    ]
