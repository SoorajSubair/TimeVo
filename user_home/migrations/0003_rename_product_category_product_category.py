# Generated by Django 4.1.3 on 2022-11-12 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0002_category_order_shippingaddress_product_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_category',
            new_name='category',
        ),
    ]
