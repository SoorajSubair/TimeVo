# Generated by Django 4.1.3 on 2022-12-07 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0058_sale_cancel_quantity_sale_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='wallet',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]