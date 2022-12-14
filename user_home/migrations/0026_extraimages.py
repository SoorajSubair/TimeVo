# Generated by Django 4.1.3 on 2022-11-22 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0025_caseshape_straptype_product_shape_product_strap'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_home.product')),
            ],
        ),
    ]
