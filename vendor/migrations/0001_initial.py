# Generated by Django 3.2.20 on 2023-08-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='vendor_register_tb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=100)),
                ('bank', models.CharField(max_length=100)),
                ('ifsc', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
            ],
        ),
    ]
