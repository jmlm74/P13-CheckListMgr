# Generated by Django 3.1.1 on 2020-10-01 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_utilities', '0005_auto_20200930_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_name',
            field=models.CharField(max_length=50, verbose_name='Mnemonic address name'),
        ),
    ]
