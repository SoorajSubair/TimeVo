# Generated by Django 4.1.3 on 2022-12-03 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0037_remove_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
