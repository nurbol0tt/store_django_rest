from django.db import models

from product.models import Product
from user.models import User


class Basket(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name_basket = models.CharField(max_length=255, blank=True, db_index=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(blank=True, default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.username


class Cart(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


class PurchasesHistory(models.Model):
    name = models.CharField(max_length=255, blank=True, db_index=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.username} - {self.quantity}"
