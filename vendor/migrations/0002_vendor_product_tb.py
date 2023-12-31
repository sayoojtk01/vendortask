# Generated by Django 3.2.20 on 2023-08-23 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='vendor_product_tb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=255)),
                ('oldprice', models.CharField(max_length=255)),
                ('newprice', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='product/')),
                ('catagory', models.CharField(max_length=255)),
                ('qty', models.CharField(max_length=255)),
                ('venid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor_register_tb')),
            ],
        ),
    ]
