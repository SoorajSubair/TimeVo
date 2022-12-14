# Generated by Django 4.1.3 on 2022-11-21 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0019_remove_orderstatus_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Order Received', 'Order Received'), ('Order Shipped', 'Order Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Order Canceled', 'Order Canceled')], default='Order Received', max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
    ]
