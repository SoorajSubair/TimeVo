# Generated by Django 4.1.3 on 2022-11-21 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0016_alter_orderitem_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processsing', models.BooleanField(default=False)),
                ('shipped', models.BooleanField(default=False)),
                ('out_for_delivery', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_home.order')),
            ],
        ),
    ]
