# Generated by Django 4.1.3 on 2022-12-01 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0035_alter_order_date_ordered_alter_orderitem_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
