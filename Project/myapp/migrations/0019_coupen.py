# Generated by Django 4.1.3 on 2022-11-27 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
