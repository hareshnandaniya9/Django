# Generated by Django 4.1.3 on 2022-11-18 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_company', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.PositiveIntegerField()),
                ('product_size', models.PositiveIntegerField()),
                ('product_image', models.ImageField(upload_to='product_image/')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
