# Generated by Django 4.1.3 on 2022-11-16 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0006_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.DeleteModel(
            name='Otp',
        ),
    ]
