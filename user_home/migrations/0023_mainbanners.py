# Generated by Django 4.1.3 on 2022-11-22 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0022_order_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainBanners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
