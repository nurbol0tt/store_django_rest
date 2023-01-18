# Generated by Django 4.1.3 on 2022-12-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_name', models.CharField(max_length=255, verbose_name='delivery_name')),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='delivery price')),
                ('delivery_method', models.CharField(choices=[('IS', 'In Store'), ('HD', 'Home Delivery'), ('DD', 'Digital Delivery')], max_length=255, verbose_name='delivery_method')),
                ('delivery_timeframe', models.CharField(max_length=255, verbose_name='delivery timeframe')),
                ('order', models.IntegerField(default=0, verbose_name='list order')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Delivery Option',
                'verbose_name_plural': 'Delivery Options',
            },
        ),
        migrations.CreateModel(
            name='PaymentSelections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='name')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Payment Selection',
                'verbose_name_plural': 'Payment Selections',
            },
        ),
    ]
