# Generated by Django 4.1.3 on 2022-12-19 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0073_cancelitem_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancelitem',
            name='category',
        ),
    ]