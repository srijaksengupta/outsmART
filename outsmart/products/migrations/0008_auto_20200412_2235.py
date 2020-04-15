# Generated by Django 2.2.6 on 2020-04-12 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productpost_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpost',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='productpost',
            name='tags',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='productpost',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]