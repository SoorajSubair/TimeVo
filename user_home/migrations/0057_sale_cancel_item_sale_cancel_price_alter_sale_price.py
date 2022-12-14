# Generated by Django 4.1.3 on 2022-12-07 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0056_alter_sale_item_alter_sale_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='cancel_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_home.cancelitem'),
        ),
        migrations.AddField(
            model_name='sale',
            name='cancel_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
