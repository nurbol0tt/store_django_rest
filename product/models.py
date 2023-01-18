# from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from user.models import User


class Manufacturer(models.Model):
    title = models.CharField(db_index=True, max_length=50)

    def __str__(self):
        return f"ID{self.id} Title: {self.title}"


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_imgs/", null=True)

    def __str__(self):
        return f"{self.id} {self.title}"


class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, blank=True, db_index=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)
    screen_size = models.DecimalField(blank=True, max_digits=5, decimal_places=2)
    processor_line = models.CharField(blank=True,  max_length=125)
    ram_size = models.IntegerField(blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, null=True)
    drive_type = models.CharField(blank=True, max_length=15)
    price = models.PositiveIntegerField(blank=True, default=0)
    quantity = models.IntegerField(blank=True, default=1)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='product_likes', default=[0])
    views = models.IntegerField(default=0)
    number_of_sales = models.IntegerField(default=0)
    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    def total_likes(self):
        return self.likes.count()


class RatingStar(models.Model):
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="star")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="product",
        related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.product.title}"


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Messages", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True,
        related_name="children"
    )
    product = models.ForeignKey(Product, verbose_name="product", on_delete=models.CASCADE,
                                null=True, related_name="reviews")

    def __str__(self):
        return f"{self.username} - {self.product}"
