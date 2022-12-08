# Generated by Django 4.1.3 on 2022-12-07 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0055_rename_order_sale_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_home.orderitem'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_home.order'),
        ),
    ]
