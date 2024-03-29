# Generated by Django 4.1.3 on 2023-04-26 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("title", models.CharField(max_length=100)),
                ("image", models.ImageField(null=True, upload_to="cat_imgs/")),
            ],
        ),
        migrations.CreateModel(
            name="Color",
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
                ("title", models.CharField(max_length=100)),
                ("color_code", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("text", models.TextField(max_length=5000, verbose_name="Messages")),
            ],
        ),
        migrations.CreateModel(
            name="Manufacturer",
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
                ("title", models.CharField(db_index=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("title", models.CharField(blank=True, db_index=True, max_length=255)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                ("description", models.TextField(blank=True)),
                (
                    "screen_size",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=5),
                ),
                ("processor_line", models.CharField(blank=True, max_length=125)),
                ("ram_size", models.IntegerField(blank=True)),
                ("drive_type", models.CharField(blank=True, max_length=15)),
                ("price", models.PositiveIntegerField(blank=True, default=0)),
                ("quantity", models.IntegerField(blank=True, default=1)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("views", models.IntegerField(default=0)),
                ("number_of_sales", models.IntegerField(default=0)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.category",
                    ),
                ),
                (
                    "color",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.color",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RatingStar",
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
                ("value", models.SmallIntegerField(default=0, verbose_name="Value")),
            ],
            options={
                "ordering": ["-value"],
            },
        ),
        migrations.CreateModel(
            name="Rating",
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
                ("ip", models.CharField(max_length=15, verbose_name="IP address")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="product.product",
                        verbose_name="product",
                    ),
                ),
                (
                    "star",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.ratingstar",
                        verbose_name="star",
                    ),
                ),
            ],
        ),
    ]
