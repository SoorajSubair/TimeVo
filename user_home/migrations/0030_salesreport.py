# Generated by Django 4.1.3 on 2022-11-29 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0029_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]
