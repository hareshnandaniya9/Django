# Generated by Django 4.1.3 on 2022-11-25 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_cart_cost_cart_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]
