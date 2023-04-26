# Generated by Django 4.1.3 on 2023-04-26 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Basket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name_basket",
                    models.CharField(blank=True, db_index=True, max_length=255),
                ),
                ("description", models.TextField(blank=True)),
                ("price", models.PositiveIntegerField(blank=True, default=0)),
                ("quantity", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="PurchasesHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, db_index=True, max_length=255)),
                ("price", models.PositiveIntegerField()),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("subtotal", models.PositiveIntegerField()),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                ("username", models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="CartProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                ("rate", models.PositiveIntegerField()),
                ("quantity", models.PositiveIntegerField()),
                ("subtotal", models.PositiveIntegerField()),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="basket.cart"
                    ),
                ),
            ],
        ),
    ]
