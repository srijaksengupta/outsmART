# Generated by Django 2.2.6 on 2020-04-21 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20200420_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpost',
            name='rating',
        ),
    ]