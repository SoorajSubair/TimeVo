# Generated by Django 4.1.3 on 2022-12-06 03:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0049_alter_order_offer_alter_order_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='cancelled',
        ),
        migrations.CreateModel(
            name='CancelItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_home.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_home.product')),
            ],
        ),
    ]
