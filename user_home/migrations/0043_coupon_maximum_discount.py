# Generated by Django 4.1.3 on 2022-12-05 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0042_coupon_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='maximum_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
